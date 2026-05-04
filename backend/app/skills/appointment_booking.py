import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Appointment
from app.skills.conflict_resolution import has_conflict
from app.skills.schedule_retrieval import ACTIVE_STATUSES


def finalize_booking(
    db: Session,
    user_id: int,
    slot: dict,
    urgency_level: str,
    constraints: dict,
    reasoning: str,
    reschedule_appointment_id: int | None = None,
) -> Appointment:
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == slot["doctor"].id,
            Appointment.status.in_(ACTIVE_STATUSES),
            Appointment.starts_at < slot["end"],
            Appointment.ends_at > slot["start"],
        )
        .all()
    )
    if has_conflict(slot, appointments):
        raise HTTPException(status_code=409, detail="Selected slot was just booked. Please retry scheduling.")

    if reschedule_appointment_id is not None:
        existing = (
            db.query(Appointment)
            .filter(Appointment.id == reschedule_appointment_id, Appointment.user_id == user_id)
            .first()
        )
        if existing is None:
            raise HTTPException(status_code=404, detail="Appointment to reschedule was not found.")
        existing.status = "rescheduled"

    appointment = Appointment(
        user_id=user_id,
        doctor_id=slot["doctor"].id,
        specialization=slot["doctor"].specialization,
        starts_at=slot["start"],
        ends_at=slot["end"],
        urgency_level=urgency_level,
        status="confirmed",
        constraints=json.dumps(constraints),
        reasoning=reasoning,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
