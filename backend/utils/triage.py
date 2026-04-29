from typing import List, Dict, Any

EMERGENCY_SYMPTOMS = [
    "chest pain", "chest pressure", "chest tightness", "chest discomfort",
    "difficulty breathing", "can't breathe", "cannot breathe", "shortness of breath",
    "trouble breathing", "breathing difficulty",
    "fainting", "passed out", "unconscious", "unresponsive", "collapsed", "fainted",
    "seizure", "convulsion", "fits", "convulsing",
    "heavy bleeding", "severe bleeding", "uncontrolled bleeding", "blood loss",
    "sudden severe headache", "worst headache", "thunderclap headache", "explosive headache",
    "sudden confusion", "sudden numbness", "sudden weakness", "face drooping",
    "arm weakness", "slurred speech", "stroke symptoms", "stroke",
    "severe allergic reaction", "anaphylaxis", "throat swelling", "tongue swelling",
    "can't swallow", "throat closing",
    "high fever infant", "fever in newborn", "fever in baby",
    "blood in vomit", "vomiting blood", "coughing blood", "hematemesis",
    "severe abdominal pain", "sudden abdominal pain", "acute abdomen",
    "blue lips", "blue fingernails", "cyanosis", "bluish skin",
    "heart attack", "cardiac arrest", "heart stopped",
    "poisoning", "overdose", "ingested poison", "drug overdose",
    "severe burn", "chemical burn", "electrical burn",
    "near drowning", "drowning",
    "diabetic coma", "hypoglycemic coma", "very low blood sugar unconscious",
    "pregnancy emergency", "eclampsia", "heavy bleeding pregnancy",
    "meningitis", "stiff neck with fever and rash",
    "severe dehydration child", "sunken eyes child", "not urinating 8 hours",
]

HIGH_RISK_SYMPTOMS = [
    "high fever", "fever above 103", "fever 103", "fever 104",
    "persistent fever", "fever for 3 days", "fever for 4 days", "fever for 5 days",
    "severe vomiting", "cannot keep fluids down", "vomiting repeatedly",
    "severe diarrhea", "blood in stool", "black stool", "tarry stool",
    "severe pain", "unbearable pain", "10 out of 10 pain",
    "rapid heart rate", "heart pounding", "palpitations severe",
    "very high blood pressure",
    "severe headache", "migraine with vision loss",
    "confusion", "disorientation", "altered consciousness",
    "difficulty swallowing", "dysphagia",
    "severe rash", "rash spreading rapidly", "hives all over",
    "jaundice", "yellow skin", "yellow eyes", "yellowing",
    "severe dizziness", "cannot stand up",
    "significant injury", "deep wound", "suspected broken bone", "fracture",
    "dengue warning signs", "belly pain vomiting bleeding dengue",
    "high fever child", "febrile seizure",
]

MEDIUM_RISK_SYMPTOMS = [
    "fever for 2 days", "persistent cough", "worsening cough",
    "ear pain", "earache", "ear infection",
    "urinary pain", "burning urination", "frequent urination pain",
    "moderate pain", "pain 5 out of 10",
    "swollen lymph nodes",
    "skin infection", "red streaks", "wound infection",
    "tooth pain severe", "dental abscess", "facial swelling",
    "eye redness", "eye discharge", "pink eye",
    "persistent vomiting", "vomiting 24 hours",
    "dehydration", "not drinking fluids", "dry mouth",
    "rash spreading", "painful rash",
    "sore throat severe", "cannot swallow liquids",
    "back pain severe", "flank pain",
]


def check_emergency_flags(symptoms: List[str], symptom_text: str = "") -> Dict[str, Any]:
    """Check symptoms against emergency and high-risk patterns."""
    combined = " ".join(symptoms).lower() + " " + symptom_text.lower()

    emergency_triggers = [kw for kw in EMERGENCY_SYMPTOMS if kw in combined]
    high_triggers = [kw for kw in HIGH_RISK_SYMPTOMS if kw in combined]

    if emergency_triggers:
        return {
            "level": "EMERGENCY",
            "color": "red",
            "score": 100,
            "triggers": emergency_triggers,
            "action": (
                "Call emergency services (911 or your local emergency number) immediately "
                "or go to the nearest emergency room now. Do NOT drive yourself."
            ),
        }

    if high_triggers:
        return {
            "level": "HIGH",
            "color": "orange",
            "score": 75,
            "triggers": high_triggers,
            "action": (
                "Seek medical attention today. Visit urgent care or call your doctor immediately. "
                "If symptoms worsen, go to the emergency room."
            ),
        }

    medium_triggers = [kw for kw in MEDIUM_RISK_SYMPTOMS if kw in combined]
    if medium_triggers:
        return {
            "level": "MEDIUM",
            "color": "yellow",
            "score": 45,
            "triggers": medium_triggers,
            "action": "Schedule a doctor appointment within 24–48 hours. Monitor symptoms closely.",
        }

    return {
        "level": "LOW",
        "color": "green",
        "score": 15,
        "triggers": [],
        "action": "Monitor symptoms at home. Rest, stay hydrated. See a doctor if symptoms worsen.",
    }


def calculate_risk_modifiers(
    age: int = None,
    temperature_f: float = None,
    duration_days: int = None,
    severity: int = None,
    existing_conditions: List[str] = None,
) -> Dict[str, Any]:
    """Calculate risk score adjustments based on patient profile."""
    modifier = 0
    reasons = []

    if age is not None:
        if age < 2:
            modifier += 25
            reasons.append("infant (under 2) — higher vulnerability")
        elif age < 5:
            modifier += 15
            reasons.append("young child — higher vulnerability")
        elif age > 75:
            modifier += 20
            reasons.append("elderly patient — higher vulnerability")
        elif age > 65:
            modifier += 10
            reasons.append("older adult — moderate additional risk")

    if temperature_f is not None:
        if temperature_f >= 104:
            modifier += 30
            reasons.append(f"very high fever ({temperature_f}°F)")
        elif temperature_f >= 103:
            modifier += 20
            reasons.append(f"high fever ({temperature_f}°F)")
        elif temperature_f >= 102:
            modifier += 10
            reasons.append(f"moderate fever ({temperature_f}°F)")
        elif temperature_f >= 100.4:
            modifier += 5
            reasons.append(f"low-grade fever ({temperature_f}°F)")

    if duration_days is not None:
        if duration_days > 7:
            modifier += 20
            reasons.append(f"symptoms lasting {duration_days} days")
        elif duration_days > 3:
            modifier += 10
            reasons.append(f"symptoms persisting {duration_days} days")

    if severity is not None and 1 <= severity <= 10:
        sev_modifier = (severity - 1) * 4
        modifier += sev_modifier
        if severity >= 7:
            reasons.append(f"high self-reported severity ({severity}/10)")

    HIGH_RISK_CONDITIONS = [
        "diabetes", "heart disease", "copd", "asthma", "immunocompromised",
        "hiv", "cancer", "kidney disease", "liver disease", "pregnancy",
        "organ transplant", "sickle cell", "lupus",
    ]
    if existing_conditions:
        matched = [
            c for c in existing_conditions
            if any(hrc in c.lower() for hrc in HIGH_RISK_CONDITIONS)
        ]
        if matched:
            modifier += 15
            reasons.append(f"high-risk underlying condition: {', '.join(matched)}")

    return {"modifier": min(modifier, 50), "reasons": reasons}


def compute_final_risk(base_score: int, modifier: int) -> Dict[str, str]:
    """Map numeric score to risk level label and color."""
    total = min(base_score + modifier, 100)

    if total >= 85:
        return {"level": "EMERGENCY", "color": "red", "score": total}
    elif total >= 60:
        return {"level": "HIGH", "color": "orange", "score": total}
    elif total >= 35:
        return {"level": "MEDIUM", "color": "yellow", "score": total}
    else:
        return {"level": "LOW", "color": "green", "score": total}
