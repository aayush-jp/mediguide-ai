from datetime import timedelta


BUCKET_HOURS = {
    "morning": range(5, 12),
    "afternoon": range(12, 17),
    "evening": range(17, 21),
    "night": list(range(0, 5)) + list(range(21, 24)),
}


def matches_preference(slot: dict, preference_profile: dict) -> bool:
    preferred = preference_profile.get("preferred_time_ranges") or []
    hour = slot["start"].hour
    return any(hour in BUCKET_HOURS.get(item.lower(), []) for item in preferred)


def schedule_efficiency_score(slot: dict, appointments_by_doctor: dict) -> int:
    appointments = appointments_by_doctor.get(slot["doctor"].id, [])
    score = 0
    for appointment in appointments:
        if abs((slot["start"] - appointment.ends_at).total_seconds()) <= 1800:
            score += 4
        if abs((appointment.starts_at - slot["end"]).total_seconds()) <= 1800:
            score += 4
    return score


def rank_slots(slots: list[dict], preference_profile: dict, urgency_level: str, appointments_by_doctor: dict) -> list[dict]:
    load_by_doctor = {
        doctor_id: len([item for item in appointments if item.starts_at <= slot_start + timedelta(days=7)])
        for doctor_id, appointments in appointments_by_doctor.items()
        for slot_start in [slots[0]["start"] if slots else None]
    }

    def score(slot: dict) -> tuple:
        pref = 1 if matches_preference(slot, preference_profile) else 0
        same_doctor = 1 if slot["doctor"].id in preference_profile.get("preferred_doctors", []) else 0
        efficiency = schedule_efficiency_score(slot, appointments_by_doctor)
        load = load_by_doctor.get(slot["doctor"].id, 0)
        minutes_from_now = int((slot["start"] - min(item["start"] for item in slots)).total_seconds() / 60)

        if urgency_level == "high":
            return (minutes_from_now, load, -same_doctor, -efficiency, -pref)
        if urgency_level == "medium":
            return (-pref, minutes_from_now, load, -same_doctor, -efficiency)
        return (-pref, -same_doctor, load, minutes_from_now, -efficiency)

    return sorted(slots, key=score)
