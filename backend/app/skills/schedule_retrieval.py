from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Appointment, Doctor


ACTIVE_STATUSES = {"confirmed", "rescheduled"}


def fetch_doctor_schedules(db: Session, specialization: str, from_time: datetime, days: int = 14) -> dict:
    until = from_time + timedelta(days=days)
    doctors = (
        db.query(Doctor)
        .filter(Doctor.specialization.ilike(f"%{specialization}%"))
        .all()
    )
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.starts_at < until,
            Appointment.ends_at > from_time,
            Appointment.status.in_(ACTIVE_STATUSES),
        )
        .all()
    )
    by_doctor: dict[str, list[Appointment]] = {}
    for appointment in appointments:
        by_doctor.setdefault(appointment.doctor_id, []).append(appointment)
    return {"doctors": doctors, "appointments_by_doctor": by_doctor, "until": until}
