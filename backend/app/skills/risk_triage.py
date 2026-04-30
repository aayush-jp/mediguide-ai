from app.skills.medical_safety import detect_emergency


def calculate_risk(symptoms: list[str], severity: int = 4, duration_days: int = 1, age: int | None = None) -> dict:
    emergency = detect_emergency(symptoms)
    if emergency["is_emergency"]:
        return {"risk_level": "Emergency", "risk_score": 100, "color": "red", "reason": emergency["message"]}

    score = severity * 7 + min(duration_days, 14) * 2
    if age is not None and (age < 5 or age > 65):
        score += 12

    if score >= 70:
        level = "High"
        reason = "Symptoms are serious, persistent, or higher risk based on the provided profile."
    elif score >= 40:
        level = "Medium"
        reason = "Symptoms need monitoring and may require medical advice if they continue."
    else:
        level = "Low"
        reason = "Symptoms appear lower risk based on the information provided."

    return {"risk_level": level, "risk_score": min(score, 99), "color": level.lower(), "reason": reason}
