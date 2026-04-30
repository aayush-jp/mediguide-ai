EMERGENCY_TERMS = {
    "chest pain",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "stroke",
    "seizure",
    "unconscious",
    "fainting",
    "severe bleeding",
    "blue lips",
    "poisoning",
    "overdose",
    "worst headache",
}


def detect_emergency(symptoms: list[str]) -> dict:
    text = " ".join(symptoms).lower()
    triggers = sorted(term for term in EMERGENCY_TERMS if term in text)
    return {
        "is_emergency": bool(triggers),
        "triggers": triggers,
        "message": "Call emergency services immediately." if triggers else "No immediate emergency red flags detected.",
    }
