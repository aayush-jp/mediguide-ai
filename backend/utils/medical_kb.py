"""
Curated medical knowledge base used by the symptom analysis tool.
Each condition has matching symptoms, risk level, and safe guidance.
"""

from typing import Dict, Any

CONDITIONS: Dict[str, Dict[str, Any]] = {
    "common_cold": {
        "name": "Common Cold",
        "icd_hint": "J00",
        "symptoms": ["runny nose", "stuffy nose", "sneezing", "sore throat", "mild cough",
                     "mild fever", "fatigue", "headache", "watery eyes"],
        "risk_level": "LOW",
        "description": "A viral infection of the upper respiratory tract, usually caused by rhinovirus.",
        "home_care": [
            "Rest and stay hydrated (water, clear soups).",
            "Use saline nasal spray to relieve congestion.",
            "Gargle with warm salt water for sore throat.",
            "Over-the-counter decongestants may help (follow label instructions).",
            "Honey in warm water can soothe throat (adults only; avoid for children under 1).",
        ],
        "when_to_see_doctor": [
            "Fever above 103°F (39.4°C) or lasting more than 3 days.",
            "Symptoms worsening after 7–10 days.",
            "Difficulty breathing or wheezing.",
            "Severe headache or sinus pain.",
            "Symptoms in infants under 3 months.",
        ],
        "typical_duration": "7–10 days",
    },
    "influenza": {
        "name": "Influenza (Flu)",
        "icd_hint": "J10/J11",
        "symptoms": ["high fever", "chills", "severe body aches", "muscle pain", "headache",
                     "fatigue", "dry cough", "sore throat", "runny nose", "vomiting", "diarrhea"],
        "risk_level": "MEDIUM",
        "description": "Flu is a contagious respiratory illness caused by influenza viruses. "
                       "It spreads easily and can be severe.",
        "home_care": [
            "Rest completely — do not push through fatigue.",
            "Drink plenty of fluids to prevent dehydration.",
            "Over-the-counter fever reducers (follow label; never give aspirin to children).",
            "Antiviral medication (oseltamivir/Tamiflu) most effective within first 48 hours — requires prescription.",
        ],
        "when_to_see_doctor": [
            "Difficulty breathing or shortness of breath.",
            "Persistent chest pain or pressure.",
            "Confusion or altered consciousness.",
            "Severe vomiting, dehydration.",
            "High-risk groups: infants, elderly, pregnant, immunocompromised.",
            "Symptoms that improve then return with worsening fever and cough.",
        ],
        "typical_duration": "7–14 days",
    },
    "covid_19": {
        "name": "COVID-19",
        "icd_hint": "U07.1",
        "symptoms": ["fever", "dry cough", "fatigue", "loss of taste", "loss of smell",
                     "sore throat", "headache", "body aches", "shortness of breath",
                     "nausea", "diarrhea", "runny nose"],
        "risk_level": "MEDIUM",
        "description": "COVID-19 is caused by SARS-CoV-2 virus. Presentation varies from mild to severe.",
        "home_care": [
            "Isolate to prevent spread.",
            "Rest and stay hydrated.",
            "Monitor oxygen levels with a pulse oximeter if possible.",
            "Antipyretics for fever (paracetamol/acetaminophen).",
            "Follow current government and WHO guidelines for treatment.",
        ],
        "when_to_see_doctor": [
            "Oxygen saturation below 94%.",
            "Difficulty breathing.",
            "Persistent chest pain.",
            "Confusion or inability to stay awake.",
            "Bluish lips or face.",
        ],
        "typical_duration": "10–14 days (mild); longer for severe cases",
    },
    "viral_fever": {
        "name": "Viral Fever",
        "icd_hint": "A99",
        "symptoms": ["fever", "body aches", "headache", "fatigue", "sore throat",
                     "runny nose", "mild cough", "loss of appetite"],
        "risk_level": "LOW",
        "description": "A non-specific viral infection causing fever and flu-like symptoms. "
                       "Very common and usually self-limiting.",
        "home_care": [
            "Rest and drink plenty of fluids.",
            "Paracetamol/acetaminophen for fever and body aches.",
            "Cool compress on forehead.",
            "Light, easy-to-digest meals.",
        ],
        "when_to_see_doctor": [
            "Fever above 103°F or lasting more than 3 days.",
            "Rash appearing with fever.",
            "Severe headache or stiff neck.",
            "Unusual drowsiness or confusion.",
        ],
        "typical_duration": "3–7 days",
    },
    "strep_throat": {
        "name": "Strep Throat",
        "icd_hint": "J02.0",
        "symptoms": ["severe sore throat", "painful swallowing", "fever", "swollen tonsils",
                     "white patches on throat", "swollen lymph nodes neck", "headache",
                     "stomach ache", "rash"],
        "risk_level": "MEDIUM",
        "description": "Bacterial throat infection caused by Group A Streptococcus. "
                       "Requires antibiotics to prevent complications like rheumatic fever.",
        "home_care": [
            "If strep is confirmed, complete the full course of antibiotics as prescribed.",
            "Warm salt water gargles for throat relief.",
            "Cold beverages or ice cream to soothe throat.",
            "Stay home until 24 hours after starting antibiotics.",
        ],
        "when_to_see_doctor": [
            "All suspected strep throat cases need a throat swab test.",
            "Difficulty breathing or drooling.",
            "Rash developing with sore throat (scarlet fever).",
            "Symptoms not improving after 48 hours of antibiotics.",
        ],
        "typical_duration": "3–5 days with antibiotics",
    },
    "uti": {
        "name": "Urinary Tract Infection (UTI)",
        "icd_hint": "N39.0",
        "symptoms": ["burning urination", "frequent urination", "urge to urinate", "cloudy urine",
                     "strong-smelling urine", "pelvic pain", "lower abdominal pain",
                     "blood in urine", "low-grade fever"],
        "risk_level": "MEDIUM",
        "description": "Bacterial infection of the urinary system. Common in women. "
                       "Requires antibiotics to prevent spread to kidneys.",
        "home_care": [
            "Drink plenty of water to flush bacteria.",
            "Urinate frequently; do not hold urine.",
            "Avoid caffeine, alcohol, and citrus juices.",
            "Heating pad on abdomen for pain relief.",
            "Cranberry products may provide mild benefit.",
        ],
        "when_to_see_doctor": [
            "All UTI symptoms should be confirmed with a urine test.",
            "Back or flank pain (may indicate kidney infection).",
            "High fever, chills, nausea — possible kidney involvement.",
            "Blood in urine.",
            "UTI in men, children, or pregnant women — always see a doctor.",
        ],
        "typical_duration": "3–7 days with antibiotics",
    },
    "gastroenteritis": {
        "name": "Gastroenteritis (Stomach Flu)",
        "icd_hint": "A09",
        "symptoms": ["nausea", "vomiting", "diarrhea", "stomach cramps", "abdominal pain",
                     "low-grade fever", "headache", "muscle aches", "loss of appetite"],
        "risk_level": "LOW",
        "description": "Inflammation of the digestive tract usually caused by a virus (norovirus, rotavirus) "
                       "or bacteria. Usually self-limiting.",
        "home_care": [
            "Stay hydrated with oral rehydration solution (ORS), clear broth, or diluted sports drinks.",
            "Eat bland foods when able: rice, bananas, toast, plain crackers (BRAT diet).",
            "Avoid dairy, fatty foods, alcohol, and caffeine.",
            "Rest.",
            "Wash hands frequently to prevent spread.",
        ],
        "when_to_see_doctor": [
            "Signs of dehydration: dry mouth, no urination for 8 hours, dizziness.",
            "Blood in stool or vomit.",
            "Fever above 102°F.",
            "Symptoms lasting more than 3 days.",
            "Infants, elderly, or immunocompromised patients.",
        ],
        "typical_duration": "1–3 days",
    },
    "food_poisoning": {
        "name": "Food Poisoning",
        "icd_hint": "A05",
        "symptoms": ["sudden nausea", "vomiting", "diarrhea", "stomach cramps", "fever",
                     "weakness", "sweating", "onset after eating"],
        "risk_level": "MEDIUM",
        "description": "Illness from eating contaminated food (bacteria, toxins, parasites). "
                       "Usually resolves with supportive care.",
        "home_care": [
            "Hydrate with ORS or clear fluids.",
            "Rest the stomach — start with clear liquids, then bland foods.",
            "Avoid solid foods while actively vomiting.",
        ],
        "when_to_see_doctor": [
            "High fever (>101.5°F) with food poisoning symptoms.",
            "Bloody diarrhea.",
            "Signs of severe dehydration.",
            "Symptoms lasting more than 3 days.",
            "Neurological symptoms: blurred vision, weakness, tingling (possible botulism).",
            "Group illness from same food source.",
        ],
        "typical_duration": "1–3 days",
    },
    "migraine": {
        "name": "Migraine",
        "icd_hint": "G43",
        "symptoms": ["severe headache", "throbbing headache", "one-sided headache",
                     "nausea", "vomiting", "light sensitivity", "sound sensitivity",
                     "visual aura", "zigzag lines vision", "dizziness"],
        "risk_level": "MEDIUM",
        "description": "A neurological condition causing intense, debilitating headaches. "
                       "Often triggered by stress, hormones, food, or sleep disruption.",
        "home_care": [
            "Rest in a dark, quiet room.",
            "Apply cold or warm compress to forehead or neck.",
            "Over-the-counter pain relievers (ibuprofen, aspirin, acetaminophen) at onset.",
            "Caffeine in small amounts can help some people.",
            "Stay hydrated.",
        ],
        "when_to_see_doctor": [
            "Worst headache of your life — seek emergency care.",
            "Headache with fever, stiff neck, rash.",
            "Sudden onset of severe headache.",
            "Headache with vision changes, weakness, confusion.",
            "Migraines becoming more frequent or severe.",
        ],
        "typical_duration": "4–72 hours",
    },
    "sinusitis": {
        "name": "Sinusitis",
        "icd_hint": "J32",
        "symptoms": ["facial pain", "facial pressure", "nasal congestion", "thick nasal discharge",
                     "post-nasal drip", "headache", "toothache upper", "fever",
                     "reduced smell", "cough"],
        "risk_level": "LOW",
        "description": "Inflammation of the sinuses, often following a cold or allergic reaction.",
        "home_care": [
            "Nasal irrigation with saline (neti pot or spray).",
            "Steam inhalation.",
            "Warm compress over face.",
            "Stay hydrated.",
            "Decongestants (short-term use only).",
        ],
        "when_to_see_doctor": [
            "Symptoms lasting more than 10 days.",
            "High fever.",
            "Severe facial pain.",
            "Swelling around eyes.",
            "Vision changes.",
            "Stiff neck.",
        ],
        "typical_duration": "Acute: 2–4 weeks",
    },
    "pneumonia": {
        "name": "Pneumonia",
        "icd_hint": "J18",
        "symptoms": ["fever", "chills", "productive cough", "chest pain breathing",
                     "shortness of breath", "fatigue", "nausea", "vomiting",
                     "confusion elderly", "rapid breathing"],
        "risk_level": "HIGH",
        "description": "Infection of the lungs (bacterial, viral, or fungal). Can be life-threatening "
                       "in high-risk groups.",
        "home_care": [],
        "when_to_see_doctor": [
            "All suspected pneumonia requires medical evaluation.",
            "Difficulty breathing or rapid breathing.",
            "Oxygen saturation below 95%.",
            "Confusion or altered mental status.",
            "High fever with productive cough.",
            "Elderly patients, infants, immunocompromised — immediate evaluation.",
        ],
        "typical_duration": "1–3 weeks with treatment",
    },
    "asthma_attack": {
        "name": "Asthma Attack",
        "icd_hint": "J45",
        "symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing",
                     "difficulty breathing", "rapid breathing", "anxiety with breathing"],
        "risk_level": "HIGH",
        "description": "Acute narrowing of the airways causing breathing difficulty. "
                       "Requires immediate action.",
        "home_care": [
            "Use prescribed rescue inhaler (salbutamol/albuterol) immediately.",
            "Sit upright, lean slightly forward.",
            "Stay calm; anxiety worsens attacks.",
            "If no improvement in 20 minutes, seek emergency care.",
        ],
        "when_to_see_doctor": [
            "No improvement after rescue inhaler.",
            "Severe difficulty breathing.",
            "Lips or fingernails turning blue.",
            "Confusion or exhaustion from breathing effort.",
            "Emergency services if severe — call 911.",
        ],
        "typical_duration": "Minutes to hours (attacks)",
    },
    "dengue": {
        "name": "Dengue Fever",
        "icd_hint": "A90",
        "symptoms": ["sudden high fever", "severe headache", "eye pain", "joint pain",
                     "muscle pain", "fatigue", "rash", "mild bleeding", "nausea", "vomiting"],
        "risk_level": "HIGH",
        "description": "Viral illness spread by Aedes mosquitoes. Common in tropical regions. "
                       "Can progress to severe dengue (dengue hemorrhagic fever).",
        "home_care": [
            "Rest and stay well hydrated.",
            "Paracetamol for fever — NEVER aspirin or ibuprofen (increases bleeding risk).",
            "Monitor for warning signs daily.",
        ],
        "when_to_see_doctor": [
            "All suspected dengue requires medical confirmation (dengue NS1 test).",
            "Warning signs: severe abdominal pain, persistent vomiting, bleeding gums/nose.",
            "Blood in stool or urine.",
            "Rapid breathing.",
            "Extreme fatigue, restlessness, or irritability.",
            "Cold or clammy skin.",
        ],
        "typical_duration": "7–10 days",
    },
    "malaria": {
        "name": "Malaria",
        "icd_hint": "B54",
        "symptoms": ["cyclical fever", "chills", "sweating", "headache", "muscle pain",
                     "nausea", "vomiting", "fatigue", "anemia symptoms"],
        "risk_level": "HIGH",
        "description": "Parasitic disease spread by Anopheles mosquitoes. Requires prompt treatment.",
        "home_care": [],
        "when_to_see_doctor": [
            "All suspected malaria requires blood test confirmation.",
            "Fever with recent travel to malaria-endemic region.",
            "Confusion, seizures, or severe headache.",
            "Difficulty breathing.",
            "Jaundice.",
        ],
        "typical_duration": "Varies by type; weeks without treatment",
    },
    "typhoid": {
        "name": "Typhoid Fever",
        "icd_hint": "A01.0",
        "symptoms": ["sustained fever", "abdominal pain", "headache", "weakness",
                     "constipation", "diarrhea", "rash rose spots", "loss of appetite"],
        "risk_level": "HIGH",
        "description": "Bacterial infection caused by Salmonella Typhi, spread through contaminated food/water.",
        "home_care": [],
        "when_to_see_doctor": [
            "All suspected typhoid requires blood/urine/stool culture.",
            "High sustained fever.",
            "Severe abdominal pain.",
            "Confusion or delirium.",
        ],
        "typical_duration": "3–4 weeks without antibiotics; shorter with treatment",
    },
    "anemia": {
        "name": "Anemia",
        "icd_hint": "D64",
        "symptoms": ["fatigue", "weakness", "pale skin", "shortness of breath on exertion",
                     "dizziness", "cold hands and feet", "headache", "brittle nails",
                     "rapid heartbeat"],
        "risk_level": "MEDIUM",
        "description": "Low red blood cell count or hemoglobin. Causes vary: iron deficiency, "
                       "B12/folate deficiency, chronic disease.",
        "home_care": [
            "Iron-rich foods: leafy greens, lentils, beans, meat, fortified cereals.",
            "Vitamin C with iron-rich foods improves absorption.",
            "Avoid tea/coffee immediately after iron-rich meals.",
        ],
        "when_to_see_doctor": [
            "Blood test (CBC) needed for diagnosis.",
            "Severe fatigue or breathlessness.",
            "Chest pain or palpitations.",
            "Anemia in children, pregnant women.",
        ],
        "typical_duration": "Weeks to months depending on cause and treatment",
    },
    "hypertension_crisis": {
        "name": "Hypertensive Crisis",
        "icd_hint": "I10",
        "symptoms": ["severe headache", "vision changes", "chest pain", "shortness of breath",
                     "nausea", "vomiting", "severe anxiety", "nosebleed"],
        "risk_level": "EMERGENCY",
        "description": "Dangerously high blood pressure (>180/120 mmHg) that can cause organ damage.",
        "home_care": [],
        "when_to_see_doctor": [
            "Immediate emergency care — call 911.",
            "Do not drive yourself.",
            "Blood pressure >180/120 with symptoms is a medical emergency.",
        ],
        "typical_duration": "Emergency — minutes matter",
    },
    "appendicitis": {
        "name": "Appendicitis",
        "icd_hint": "K37",
        "symptoms": ["pain around navel", "pain moving to lower right abdomen", "fever",
                     "nausea", "vomiting", "loss of appetite", "pain worsens with movement",
                     "rebound tenderness"],
        "risk_level": "EMERGENCY",
        "description": "Inflammation of the appendix. Requires surgical evaluation. "
                       "Can rupture if untreated.",
        "home_care": [],
        "when_to_see_doctor": [
            "Emergency — go to ER immediately.",
            "Do not eat, drink, or take pain medication that might mask symptoms.",
            "Do not apply heat to abdomen.",
        ],
        "typical_duration": "Emergency surgical condition",
    },
    "dehydration": {
        "name": "Dehydration",
        "icd_hint": "E86",
        "symptoms": ["dry mouth", "thirst", "dark urine", "decreased urination",
                     "dizziness", "fatigue", "headache", "dry skin", "sunken eyes"],
        "risk_level": "MEDIUM",
        "description": "Insufficient fluids in the body. Can range from mild to life-threatening.",
        "home_care": [
            "Oral rehydration solution (ORS) — most effective.",
            "Small sips of water or clear fluids frequently.",
            "Avoid sugary drinks.",
            "Electrolyte drinks (sports drinks diluted 50%).",
        ],
        "when_to_see_doctor": [
            "No urination for 8+ hours.",
            "Extreme thirst with confusion.",
            "Sunken eyes, very dry mouth.",
            "Rapid heartbeat.",
            "Severe dehydration in infants, elderly, or after prolonged vomiting/diarrhea.",
        ],
        "typical_duration": "Hours with proper rehydration",
    },
    "heat_stroke": {
        "name": "Heat Stroke",
        "icd_hint": "T67.0",
        "symptoms": ["body temperature above 104f", "hot dry skin", "confusion",
                     "rapid heartbeat", "nausea", "vomiting", "headache",
                     "loss of consciousness"],
        "risk_level": "EMERGENCY",
        "description": "Life-threatening condition where body temperature regulation fails. "
                       "Can cause organ damage in minutes.",
        "home_care": [],
        "when_to_see_doctor": [
            "Call 911 immediately.",
            "Move person to cool environment.",
            "Apply ice packs to armpits, groin, neck while waiting for help.",
            "Do NOT give fluids to unconscious person.",
        ],
        "typical_duration": "Emergency condition",
    },
    "chickenpox": {
        "name": "Chickenpox (Varicella)",
        "icd_hint": "B01",
        "symptoms": ["itchy blisters", "fever", "fatigue", "loss of appetite",
                     "headache", "rash starting on trunk", "blisters all stages simultaneously"],
        "risk_level": "LOW",
        "description": "Viral infection causing itchy blisters. Very contagious but usually mild in children.",
        "home_care": [
            "Calamine lotion for itch relief.",
            "Cool baths with baking soda or oatmeal.",
            "Trim fingernails to prevent scratching and infection.",
            "Loose, comfortable clothing.",
            "Paracetamol for fever — NEVER aspirin in children (Reye's syndrome risk).",
            "Isolate until all blisters have crusted over.",
        ],
        "when_to_see_doctor": [
            "High fever or fever returning after improvement.",
            "Rash with severe pain, redness, or warmth (secondary infection).",
            "Rash near eyes.",
            "Breathing difficulty.",
            "Chickenpox in adults, pregnant women, newborns, or immunocompromised.",
        ],
        "typical_duration": "5–10 days (rash); 2–3 weeks total",
    },
    "conjunctivitis": {
        "name": "Conjunctivitis (Pink Eye)",
        "icd_hint": "H10",
        "symptoms": ["red eyes", "eye discharge", "watery eyes", "itchy eyes",
                     "crusty eyes morning", "gritty feeling eye", "light sensitivity"],
        "risk_level": "LOW",
        "description": "Inflammation of the conjunctiva. Can be viral, bacterial, or allergic.",
        "home_care": [
            "Clean eyelids with warm, damp cloth.",
            "Do not touch eyes with hands.",
            "Wash hands frequently.",
            "Do not share towels or pillowcases.",
            "Antihistamine eye drops for allergic conjunctivitis.",
        ],
        "when_to_see_doctor": [
            "Bacterial conjunctivitis needs antibiotic eye drops — see a doctor.",
            "Vision changes.",
            "Severe eye pain.",
            "Symptoms in newborns (urgent).",
            "No improvement after 2–3 days.",
        ],
        "typical_duration": "5–7 days (viral); shorter with antibiotics (bacterial)",
    },
}


def get_condition(condition_key: str) -> Dict[str, Any]:
    return CONDITIONS.get(condition_key, {})


def match_symptoms_to_conditions(symptoms: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
    """Simple keyword overlap scoring to rank conditions by symptom match."""
    from typing import List as L
    symptom_text = " ".join(symptoms).lower()

    scores = []
    for key, cond in CONDITIONS.items():
        matched = sum(1 for s in cond["symptoms"] if s in symptom_text)
        if matched > 0:
            confidence = min(round((matched / len(cond["symptoms"])) * 100), 95)
            scores.append({
                "key": key,
                "name": cond["name"],
                "confidence": confidence,
                "matched_symptoms": matched,
                "risk_level": cond["risk_level"],
                "description": cond["description"],
                "when_to_see_doctor": cond.get("when_to_see_doctor", []),
                "home_care": cond.get("home_care", []),
                "typical_duration": cond.get("typical_duration", "Varies"),
            })

    scores.sort(key=lambda x: (-x["confidence"], -x["matched_symptoms"]))
    return scores[:top_n]


# Normal lab reference ranges
LAB_RANGES = {
    "hemoglobin": {
        "unit": "g/dL",
        "male": {"low": 13.5, "high": 17.5},
        "female": {"low": 12.0, "high": 15.5},
        "general": {"low": 12.0, "high": 17.5},
    },
    "wbc": {
        "unit": "×10³/μL",
        "general": {"low": 4.5, "high": 11.0},
    },
    "platelets": {
        "unit": "×10³/μL",
        "general": {"low": 150, "high": 400},
    },
    "blood_glucose_fasting": {
        "unit": "mg/dL",
        "general": {"low": 70, "high": 99},
    },
    "blood_glucose_random": {
        "unit": "mg/dL",
        "general": {"low": 70, "high": 140},
    },
    "hba1c": {
        "unit": "%",
        "general": {"low": 0, "high": 5.6},
    },
    "creatinine": {
        "unit": "mg/dL",
        "male": {"low": 0.7, "high": 1.3},
        "female": {"low": 0.6, "high": 1.1},
        "general": {"low": 0.6, "high": 1.3},
    },
    "alt": {
        "unit": "U/L",
        "general": {"low": 7, "high": 56},
    },
    "ast": {
        "unit": "U/L",
        "general": {"low": 10, "high": 40},
    },
    "total_cholesterol": {
        "unit": "mg/dL",
        "general": {"low": 0, "high": 200},
    },
    "ldl": {
        "unit": "mg/dL",
        "general": {"low": 0, "high": 100},
    },
    "hdl": {
        "unit": "mg/dL",
        "male": {"low": 40, "high": 60},
        "female": {"low": 50, "high": 60},
        "general": {"low": 40, "high": 60},
    },
    "triglycerides": {
        "unit": "mg/dL",
        "general": {"low": 0, "high": 150},
    },
    "tsh": {
        "unit": "mIU/L",
        "general": {"low": 0.4, "high": 4.0},
    },
    "vitamin_d": {
        "unit": "ng/mL",
        "general": {"low": 20, "high": 100},
    },
    "vitamin_b12": {
        "unit": "pg/mL",
        "general": {"low": 200, "high": 900},
    },
    "ferritin": {
        "unit": "ng/mL",
        "male": {"low": 24, "high": 336},
        "female": {"low": 11, "high": 307},
        "general": {"low": 11, "high": 336},
    },
    "sodium": {
        "unit": "mEq/L",
        "general": {"low": 136, "high": 145},
    },
    "potassium": {
        "unit": "mEq/L",
        "general": {"low": 3.5, "high": 5.0},
    },
    "uric_acid": {
        "unit": "mg/dL",
        "male": {"low": 3.4, "high": 7.0},
        "female": {"low": 2.4, "high": 6.0},
        "general": {"low": 2.4, "high": 7.0},
    },
}


def interpret_lab_value(test_name: str, value: float, gender: str = None) -> Dict[str, Any]:
    """Interpret a single lab value against normal ranges."""
    key = test_name.lower().replace(" ", "_").replace("-", "_")
    if key not in LAB_RANGES:
        return {"status": "unknown", "interpretation": "Reference range not available in our database."}

    ref = LAB_RANGES[key]
    unit = ref["unit"]

    # Pick gender-specific range if available
    if gender and gender.lower() in ref:
        range_data = ref[gender.lower()]
    else:
        range_data = ref.get("general", ref.get("male", {}))

    low = range_data.get("low", 0)
    high = range_data.get("high", float("inf"))

    if value < low:
        status = "LOW"
        severity = "critical" if value < low * 0.7 else "mild"
    elif value > high:
        status = "HIGH"
        severity = "critical" if value > high * 1.5 else "mild"
    else:
        status = "NORMAL"
        severity = "none"

    return {
        "status": status,
        "severity": severity,
        "normal_range": f"{low}–{high} {unit}",
        "unit": unit,
    }
