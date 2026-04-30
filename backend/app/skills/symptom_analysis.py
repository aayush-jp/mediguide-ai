from app.skills.risk_triage import calculate_risk


FOLLOW_UPS = [
    "How long have these symptoms been present?",
    "How severe are the symptoms on a scale of 1 to 10?",
    "Do you have fever, chest pain, breathing difficulty, or any existing conditions?",
]


def analyze_symptoms(symptoms: list[str], age: int | None, duration_days: int | None, severity: int | None) -> dict:
    risk = calculate_risk(symptoms, severity or 4, duration_days or 1, age)
    symptom_text = " ".join(symptoms).lower()
    possible = []

    if any(term in symptom_text for term in ["fever", "cough", "sore throat", "cold"]):
        possible.append({"condition": "Viral respiratory infection", "confidence": 72})
    if any(term in symptom_text for term in ["headache", "nausea", "vomit"]):
        possible.append({"condition": "Migraine, dehydration, or gastrointestinal illness", "confidence": 58})
    if any(term in symptom_text for term in ["stomach", "abdominal", "diarrhea"]):
        possible.append({"condition": "Digestive upset or food-related illness", "confidence": 61})
    if not possible:
        possible.append({"condition": "Non-specific symptoms requiring more context", "confidence": 42})

    return {
        **risk,
        "possible_conditions": possible,
        "follow_up_questions": FOLLOW_UPS,
        "recommendation": doctor_recommendation(risk["risk_level"]),
        "disclaimer": "This is not a final diagnosis. Consult a licensed medical professional for personal advice.",
    }


def doctor_recommendation(risk_level: str) -> str:
    if risk_level == "Emergency":
        return "Seek emergency care now."
    if risk_level == "High":
        return "Consult a doctor today."
    if risk_level == "Medium":
        return "Consult a doctor if symptoms persist, worsen, or remain unclear."
    return "Self-monitor and use supportive care. See a doctor if symptoms persist or become serious."
