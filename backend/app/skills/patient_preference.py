from collections import Counter
from datetime import datetime

from app.models import Appointment


def time_bucket(value: datetime) -> str:
    hour = value.hour
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "night"


def build_preference_profile(history: list[Appointment], requested_ranges: list[str]) -> dict:
    completed_like = [item for item in history if item.status in {"confirmed", "completed"}]
    missed_or_cancelled = [item for item in history if item.status in {"cancelled", "missed"}]

    time_counts = Counter(time_bucket(item.starts_at) for item in completed_like)
    day_counts = Counter(item.starts_at.strftime("%A") for item in completed_like)
    doctor_counts = Counter(item.doctor_id for item in completed_like)

    explicit_ranges = [item.strip().lower() for item in requested_ranges if item.strip()]
    learned_ranges = [name for name, _ in time_counts.most_common(2)]

    return {
        "preferred_time_ranges": explicit_ranges or learned_ranges or ["morning"],
        "learned_time_patterns": dict(time_counts),
        "preferred_days": [name for name, _ in day_counts.most_common(3)],
        "preferred_doctors": [name for name, _ in doctor_counts.most_common(3)],
        "missed_or_cancelled_count": len(missed_or_cancelled),
        "no_show_probability": min(0.65, len(missed_or_cancelled) / max(len(history), 1)),
    }
