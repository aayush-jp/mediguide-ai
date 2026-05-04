from app.models import Appointment


def has_conflict(candidate: dict, appointments: list[Appointment]) -> bool:
    return any(item.starts_at < candidate["end"] and item.ends_at > candidate["start"] for item in appointments)


def explain_tradeoffs(urgency_level: str, preference_matched: bool) -> str:
    if urgency_level == "high" and not preference_matched:
        return "High urgency required the earliest conflict-free slot, overriding preferred timing."
    if preference_matched:
        return "Recommended slot matches patient timing preference and doctor availability."
    return "No ideal preferred slot was available; alternatives balance earlier access and comfort."
