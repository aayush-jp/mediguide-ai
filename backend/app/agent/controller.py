from app.skills.disease_prediction import predict_disease
from app.skills.doctor_escalation import escalation_advice
from app.skills.medical_safety import detect_emergency
from app.skills.multilingual_response import localize_response
from app.skills.symptom_analysis import analyze_symptoms
from app.skills.availability_analysis import find_valid_slots
from app.skills.conflict_resolution import explain_tradeoffs
from app.skills.patient_preference import build_preference_profile
from app.skills.schedule_optimization import matches_preference, rank_slots
from app.skills.schedule_retrieval import fetch_doctor_schedules


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

    def run_appointment_scheduler(
        self,
        db,
        user,
        preferred_time_ranges: list[str],
        urgency_level: str,
        specialization: str,
        current_datetime,
        constraints: dict,
        duration_minutes: int,
    ) -> dict:
        history = list(user.appointments)
        preference_profile = build_preference_profile(history, preferred_time_ranges)
        schedules = fetch_doctor_schedules(db, specialization, current_datetime)
        valid_slots = find_valid_slots(
            schedules["doctors"],
            schedules["appointments_by_doctor"],
            current_datetime,
            duration_minutes,
            constraints,
        )
        ranked = rank_slots(valid_slots, preference_profile, urgency_level, schedules["appointments_by_doctor"])

        recommended = ranked[0] if ranked else None
        alternatives = ranked[1:4] if recommended else ranked[:3]
        preference_matched = bool(recommended and matches_preference(recommended, preference_profile))

        if urgency_level == "high":
            urgency_handling = "prioritized earliest conflict-free slot"
        elif urgency_level == "medium":
            urgency_handling = "balanced patient preference with earliest availability"
        else:
            urgency_handling = "strongly prioritized patient comfort and preferred timing"

        reasoning = (
            explain_tradeoffs(urgency_level, preference_matched)
            if recommended
            else "No conflict-free doctor slot matched the specialization and constraints in the search window."
        )

        return {
            "recommended": recommended,
            "alternatives": alternatives,
            "preference_profile": preference_profile,
            "reasoning": reasoning,
            "urgency_handling": urgency_handling,
        }


medical_agent = MedicalAgentController()
