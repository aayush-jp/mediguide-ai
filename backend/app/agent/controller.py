from app.skills.disease_prediction import predict_disease
from app.skills.doctor_escalation import escalation_advice
from app.skills.medical_safety import detect_emergency
from app.skills.multilingual_response import localize_response
from app.skills.symptom_analysis import analyze_symptoms


class MedicalAgentController:
    def run_symptom_pipeline(
        self,
        symptoms: list[str],
        age: int | None,
        duration_days: int | None,
        severity: int | None,
        language: str,
    ) -> dict:
        analysis = analyze_symptoms(symptoms, age, duration_days, severity)
        analysis["doctor_escalation"] = escalation_advice(analysis["risk_level"])
        analysis["narrative"] = localize_response(
            "MediGuide AI reviewed your symptoms, checked emergency red flags, estimated risk, and prepared safe next steps.",
            language,
        )
        return analysis

    def run_chat(self, message: str, language: str) -> dict:
        emergency = detect_emergency([message])
        response = "I can help assess symptoms. Please share duration, severity, age, and any red flags."
        if emergency["is_emergency"]:
            response = "This may be a medical emergency. Call emergency services immediately."
        return {"response": localize_response(response, language), **emergency}

    def run_prediction(self, symptoms: list[str], age: int | None, duration_days: int | None) -> dict:
        return predict_disease(symptoms, age, duration_days)


medical_agent = MedicalAgentController()
