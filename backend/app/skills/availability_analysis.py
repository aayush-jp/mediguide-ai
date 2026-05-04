from datetime import datetime, time, timedelta

from app.models import Appointment, Doctor


def parse_clock(value: str) -> time:
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


def overlaps(start: datetime, end: datetime, appointments: list[Appointment]) -> bool:
    return any(item.starts_at < end and item.ends_at > start for item in appointments)


def doctor_matches_constraints(doctor: Doctor, constraints: dict) -> bool:
    location = (constraints.get("location") or "").strip().lower()
    gender = (constraints.get("gender_preference") or "").strip().lower()
    language = (constraints.get("language") or "").strip().lower()

    if location and location not in doctor.location.lower():
        return False
    if gender and gender != doctor.gender.lower():
        return False
    if language and language not in doctor.languages.lower():
        return False
    return True


def find_valid_slots(
    doctors: list[Doctor],
    appointments_by_doctor: dict[str, list[Appointment]],
    from_time: datetime,
    duration_minutes: int,
    constraints: dict,
    days: int = 14,
) -> list[dict]:
    slots: list[dict] = []
    search_start = from_time.replace(second=0, microsecond=0)
    if search_start.minute not in (0, 30):
        next_minute = 30 if search_start.minute < 30 else 60
        search_start = search_start.replace(minute=0) + timedelta(minutes=next_minute)

    for doctor in doctors:
        if not doctor_matches_constraints(doctor, constraints):
            continue

        working_days = {int(day) for day in doctor.working_days.split(",") if day != ""}
        work_start = parse_clock(doctor.working_start)
        work_end = parse_clock(doctor.working_end)
        duration = timedelta(minutes=duration_minutes or doctor.appointment_duration_minutes)
        doctor_appointments = appointments_by_doctor.get(doctor.id, [])

        for offset in range(days):
            day = search_start.date() + timedelta(days=offset)
            if day.weekday() not in working_days:
                continue

            cursor = datetime.combine(day, work_start)
            end_of_day = datetime.combine(day, work_end)
            if cursor < search_start:
                cursor = search_start

            if cursor.minute not in (0, 30):
                cursor = cursor.replace(minute=30 if cursor.minute < 30 else 0)
                if cursor.minute == 0:
                    cursor += timedelta(hours=1)

            while cursor + duration <= end_of_day:
                slot_end = cursor + duration
                if cursor >= search_start and not overlaps(cursor, slot_end, doctor_appointments):
                    slots.append({"doctor": doctor, "start": cursor, "end": slot_end})
                cursor += timedelta(minutes=30)

    return slots
