from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agent.controller import medical_agent
from app.database import get_db
from app.models import Appointment, User
from app.schemas import (
    AppointmentOut,
    AppointmentRescheduleRequest,
    AppointmentScheduleRequest,
    AppointmentScheduleResponse,
    AppointmentSlot,
)
from app.security import get_current_user
from app.skills.appointment_booking import finalize_booking

router = APIRouter(prefix="/api/appointments", tags=["Dynamic Appointment Scheduling"])


def serialize_slot(slot: dict | None) -> AppointmentSlot | None:
    if slot is None:
        return None
    start = slot["start"]
    doctor = slot["doctor"]
    return AppointmentSlot(
        date=start.strftime("%Y-%m-%d"),
        time=start.strftime("%I:%M %p"),
        doctor_id=doctor.id,
        doctor_name=doctor.name,
        specialization=doctor.specialization,
    )


def serialize_appointment(item: Appointment) -> AppointmentOut:
    return AppointmentOut(
        id=item.id,
        doctor_id=item.doctor_id,
        doctor_name=item.doctor.name,
        specialization=item.specialization,
        starts_at=item.starts_at,
        ends_at=item.ends_at,
        urgency_level=item.urgency_level,
        status=item.status,
        reasoning=item.reasoning,
    )


def run_schedule(
    payload: AppointmentScheduleRequest,
    current_user: User,
    db: Session,
    reschedule_appointment_id: int | None = None,
) -> AppointmentScheduleResponse:
    if payload.patient_id is not None and payload.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Patient ID does not match the authenticated user.")

    now = (payload.current_datetime or datetime.now()).replace(second=0, microsecond=0)
    constraints = payload.constraints.model_dump()
    result = medical_agent.run_appointment_scheduler(
        db=db,
        user=current_user,
        preferred_time_ranges=payload.preferred_time_ranges,
        urgency_level=payload.urgency_level,
        specialization=payload.doctor_specialization_required,
        current_datetime=now,
        constraints=constraints,
        duration_minutes=payload.appointment_duration_minutes,
    )

    recommended = result["recommended"]
    alternatives = [serialize_slot(slot) for slot in result["alternatives"]]

    if recommended is None:
        return AppointmentScheduleResponse(
            recommended_slot=None,
            alternative_slots=[],
            reasoning=result["reasoning"],
            urgency_handling=result["urgency_handling"],
            status="conflict",
            preference_profile=result["preference_profile"],
        )

    appointment_id = None
    status = "suggestion"
    if payload.confirm_booking:
        appointment = finalize_booking(
            db,
            current_user.id,
            recommended,
            payload.urgency_level,
            constraints,
            result["reasoning"],
            reschedule_appointment_id=reschedule_appointment_id,
        )
        appointment_id = appointment.id
        status = "confirmed"

    return AppointmentScheduleResponse(
        recommended_slot=serialize_slot(recommended),
        alternative_slots=alternatives,
        reasoning=result["reasoning"],
        urgency_handling=result["urgency_handling"],
        status=status,
        appointment_id=appointment_id,
        preference_profile=result["preference_profile"],
    )


@router.post("/schedule", response_model=AppointmentScheduleResponse)
def schedule_appointment(
    payload: AppointmentScheduleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return run_schedule(payload, current_user, db)


@router.post("/reschedule", response_model=AppointmentScheduleResponse)
def reschedule_appointment(
    payload: AppointmentRescheduleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Appointment).filter(Appointment.id == payload.appointment_id, Appointment.user_id == current_user.id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return run_schedule(payload, current_user, db, reschedule_appointment_id=payload.appointment_id)


@router.post("/{appointment_id}/cancel", response_model=AppointmentOut)
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.user_id == current_user.id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    appointment.status = "cancelled"
    db.commit()
    db.refresh(appointment)
    return serialize_appointment(appointment)


@router.get("", response_model=list[AppointmentOut])
def list_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = (
        db.query(Appointment)
        .filter(Appointment.user_id == current_user.id)
        .order_by(Appointment.starts_at.desc())
        .all()
    )
    return [serialize_appointment(item) for item in items]
