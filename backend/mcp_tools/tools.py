"""
Concrete implementations of MediGuide AI medical tools.
These are called both by the Claude agent (via tool_use) and exposed via MCP server.
"""

import json
import base64
from typing import Any, Dict, List, Optional
import anthropic

from backend.config import settings
from backend.utils.triage import (
    check_emergency_flags,
    calculate_risk_modifiers,
    compute_final_risk,
)
from backend.utils.medical_kb import (
    match_symptoms_to_conditions,
    get_condition,
    interpret_lab_value,
    LAB_RANGES,
)


# ---------------------------------------------------------------------------
# Tool: Emergency Check
# ---------------------------------------------------------------------------

def tool_check_emergency_flags(
    symptoms: List[str],
    symptom_text: str = "",
) -> Dict[str, Any]:
    """Detect emergency red-flag symptoms that require immediate action."""
    return check_emergency_flags(symptoms, symptom_text)


# ---------------------------------------------------------------------------
# Tool: Symptom Analyzer
# ---------------------------------------------------------------------------

def tool_analyze_symptoms(
    symptoms: List[str],
    age: Optional[int] = None,
    gender: Optional[str] = None,
    duration_days: Optional[int] = None,
    severity: Optional[int] = None,
    temperature_f: Optional[float] = None,
    existing_conditions: Optional[List[str]] = None,
    allergies: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Match reported symptoms against the condition knowledge base and
    apply patient-profile risk modifiers.
    """
    matches = match_symptoms_to_conditions(symptoms, top_n=5)
    modifiers = calculate_risk_modifiers(
        age=age,
        temperature_f=temperature_f,
        duration_days=duration_days,
        severity=severity,
        existing_conditions=existing_conditions or [],
    )

    # Compute final risk using highest-confidence match as base
    base_score = 15
    if matches:
        top_match_risk = matches[0]["risk_level"]
        risk_map = {"LOW": 15, "MEDIUM": 45, "HIGH": 75, "EMERGENCY": 100}
        base_score = risk_map.get(top_match_risk, 15)

    final_risk = compute_final_risk(base_score, modifiers["modifier"])

    return {
        "possible_conditions": matches,
        "risk_assessment": final_risk,
        "risk_modifiers": modifiers,
        "symptom_count": len(symptoms),
        "note": (
            "These are possible conditions based on symptom pattern matching. "
            "This is NOT a diagnosis. Always consult a qualified healthcare professional."
        ),
    }


# ---------------------------------------------------------------------------
# Tool: Risk Calculator
# ---------------------------------------------------------------------------

def tool_calculate_risk(
    base_level: str,
    age: Optional[int] = None,
    temperature_f: Optional[float] = None,
    duration_days: Optional[int] = None,
    severity: Optional[int] = None,
    existing_conditions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Calculate the final risk level with patient-profile modifiers."""
    risk_map = {"LOW": 15, "MEDIUM": 45, "HIGH": 75, "EMERGENCY": 100}
    base_score = risk_map.get(base_level.upper(), 15)

    modifiers = calculate_risk_modifiers(
        age=age,
        temperature_f=temperature_f,
        duration_days=duration_days,
        severity=severity,
        existing_conditions=existing_conditions or [],
    )
    final = compute_final_risk(base_score, modifiers["modifier"])
    final["reasons"] = modifiers["reasons"]
    return final


# ---------------------------------------------------------------------------
# Tool: Lab Value Interpreter
# ---------------------------------------------------------------------------

def tool_interpret_lab_values(
    values: Dict[str, float],
    gender: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Interpret a dictionary of lab results {test_name: numeric_value}
    against normal reference ranges.
    """
    results = []
    for test_name, value in values.items():
        interp = interpret_lab_value(test_name, value, gender)
        results.append({
            "test": test_name,
            "value": value,
            **interp,
        })
    return results


# ---------------------------------------------------------------------------
# Tool: Medical Info Retrieval
# ---------------------------------------------------------------------------

def tool_get_medical_info(condition_key: str) -> Dict[str, Any]:
    """Retrieve detailed information about a specific condition from the knowledge base."""
    cond = get_condition(condition_key)
    if not cond:
        return {"error": f"Condition '{condition_key}' not found in knowledge base."}
    return cond


# ---------------------------------------------------------------------------
# Tool: Doctor Referral Decider
# ---------------------------------------------------------------------------

def tool_doctor_referral_rule(
    risk_level: str,
    duration_days: Optional[int] = None,
    age: Optional[int] = None,
    existing_conditions: Optional[List[str]] = None,
    symptom_text: str = "",
) -> Dict[str, Any]:
    """
    Determine whether and how urgently the user should see a doctor,
    based on risk level and patient profile.
    """
    level = risk_level.upper()

    if level == "EMERGENCY":
        return {
            "referral_needed": True,
            "urgency": "IMMEDIATE",
            "message": (
                "Call emergency services (911) or go to the nearest emergency room NOW. "
                "Do not drive yourself. This is a medical emergency."
            ),
            "referral_type": "Emergency Room",
        }
    elif level == "HIGH":
        return {
            "referral_needed": True,
            "urgency": "TODAY",
            "message": (
                "You should see a doctor or visit urgent care today. "
                "If symptoms worsen rapidly, go to the emergency room."
            ),
            "referral_type": "Urgent Care or Doctor",
        }
    elif level == "MEDIUM":
        # Additional escalation for vulnerable groups
        vulnerable = (
            (age is not None and (age < 5 or age > 65))
            or bool(existing_conditions)
            or (duration_days is not None and duration_days > 5)
        )
        if vulnerable:
            return {
                "referral_needed": True,
                "urgency": "WITHIN 24 HOURS",
                "message": (
                    "Given your age, medical history, or duration of symptoms, "
                    "please see a doctor within 24 hours."
                ),
                "referral_type": "Primary Care Doctor",
            }
        return {
            "referral_needed": True,
            "urgency": "WITHIN 48 HOURS",
            "message": (
                "Schedule a doctor appointment within the next 1–2 days. "
                "Monitor for any worsening signs."
            ),
            "referral_type": "Primary Care Doctor",
        }
    else:  # LOW
        return {
            "referral_needed": False,
            "urgency": "AS NEEDED",
            "message": (
                "You can monitor your symptoms at home. Rest, stay hydrated, and "
                "see a doctor if symptoms persist beyond 5 days, worsen, or new "
                "concerning symptoms appear."
            ),
            "referral_type": "None required currently",
        }


# ---------------------------------------------------------------------------
# Tool: OCR / Report Analysis via Claude Vision
# ---------------------------------------------------------------------------

async def tool_analyze_report_image(
    image_data: str,
    media_type: str = "image/jpeg",
    gender: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Use Claude Vision to extract and interpret values from a medical report image.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    extraction_prompt = """You are a medical report analyst assistant.
Analyze this medical report image and extract ALL test values.

Return a JSON object with this exact structure:
{
  "report_type": "blood test / urine test / X-ray / other",
  "patient_info": {"name": "if visible", "date": "if visible", "age": "if visible"},
  "values": {
    "test_name_lowercase_underscore": numeric_value_only,
    ...
  },
  "raw_text_summary": "brief summary of what the report contains",
  "special_notes": ["any doctor notes or flagged values already marked in the report"]
}

Use standard test name keys like: hemoglobin, wbc, platelets, blood_glucose_fasting,
hba1c, creatinine, alt, ast, total_cholesterol, ldl, hdl, triglycerides, tsh,
vitamin_d, vitamin_b12, ferritin, sodium, potassium, uric_acid.

Return ONLY the JSON object, no markdown."""

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": extraction_prompt},
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()
    # Strip possible markdown code fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        extracted = json.loads(raw)
    except json.JSONDecodeError:
        extracted = {"raw_text_summary": raw, "values": {}}

    # Interpret extracted values
    interpretations = []
    for test, value in extracted.get("values", {}).items():
        if isinstance(value, (int, float)):
            interp = interpret_lab_value(test, float(value), gender)
            interpretations.append({
                "test": test,
                "value": value,
                **interp,
            })

    return {
        "report_type": extracted.get("report_type", "Unknown"),
        "patient_info": extracted.get("patient_info", {}),
        "raw_summary": extracted.get("raw_text_summary", ""),
        "special_notes": extracted.get("special_notes", []),
        "interpreted_values": interpretations,
        "disclaimer": (
            "This analysis is for informational purposes only. "
            "Consult your doctor or pathologist for medical interpretation."
        ),
    }


# ---------------------------------------------------------------------------
# Anthropic tool_use schema definitions (used by the agent)
# ---------------------------------------------------------------------------

AGENT_TOOLS = [
    {
        "name": "check_emergency_flags",
        "description": (
            "Check whether the patient's reported symptoms include emergency red flags "
            "that require calling 911 or visiting an emergency room immediately. "
            "Always call this first when symptoms are reported."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symptoms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of symptoms the patient reported",
                },
                "symptom_text": {
                    "type": "string",
                    "description": "Full free-text description of symptoms (optional)",
                },
            },
            "required": ["symptoms"],
        },
    },
    {
        "name": "analyze_symptoms",
        "description": (
            "Match reported symptoms against the medical knowledge base to find possible "
            "conditions and calculate a risk level. Returns top matching conditions with "
            "confidence scores, home care advice, and when to see a doctor."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symptoms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of symptoms",
                },
                "age": {"type": "integer", "description": "Patient age in years"},
                "gender": {
                    "type": "string",
                    "enum": ["male", "female", "other"],
                    "description": "Patient gender",
                },
                "duration_days": {
                    "type": "integer",
                    "description": "How many days the symptoms have been present",
                },
                "severity": {
                    "type": "integer",
                    "description": "Self-reported severity on a scale of 1–10",
                },
                "temperature_f": {
                    "type": "number",
                    "description": "Body temperature in Fahrenheit",
                },
                "existing_conditions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Known medical conditions the patient has",
                },
                "allergies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Known medication or food allergies",
                },
            },
            "required": ["symptoms"],
        },
    },
    {
        "name": "calculate_risk",
        "description": "Calculate the final risk level with patient-profile modifiers applied.",
        "input_schema": {
            "type": "object",
            "properties": {
                "base_level": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "EMERGENCY"],
                    "description": "Initial risk level from symptom analysis",
                },
                "age": {"type": "integer"},
                "temperature_f": {"type": "number"},
                "duration_days": {"type": "integer"},
                "severity": {"type": "integer"},
                "existing_conditions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["base_level"],
        },
    },
    {
        "name": "doctor_referral_rule",
        "description": (
            "Determine whether, when, and how urgently the patient should see a doctor, "
            "based on their risk level and profile."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "risk_level": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "EMERGENCY"],
                },
                "duration_days": {"type": "integer"},
                "age": {"type": "integer"},
                "existing_conditions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "symptom_text": {"type": "string"},
            },
            "required": ["risk_level"],
        },
    },
    {
        "name": "interpret_lab_values",
        "description": (
            "Interpret numeric lab test results against standard reference ranges. "
            "Use this when analyzing uploaded medical reports."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "values": {
                    "type": "object",
                    "description": "Dictionary of {test_name: numeric_value}",
                    "additionalProperties": {"type": "number"},
                },
                "gender": {
                    "type": "string",
                    "enum": ["male", "female"],
                    "description": "Patient gender for gender-specific ranges",
                },
            },
            "required": ["values"],
        },
    },
    {
        "name": "get_medical_info",
        "description": "Retrieve detailed information about a specific condition from the knowledge base.",
        "input_schema": {
            "type": "object",
            "properties": {
                "condition_key": {
                    "type": "string",
                    "description": (
                        "Condition key such as: common_cold, influenza, covid_19, viral_fever, "
                        "strep_throat, uti, gastroenteritis, food_poisoning, migraine, sinusitis, "
                        "pneumonia, asthma_attack, dengue, malaria, typhoid, anemia, "
                        "hypertension_crisis, appendicitis, dehydration, heat_stroke, "
                        "chickenpox, conjunctivitis"
                    ),
                }
            },
            "required": ["condition_key"],
        },
    },
]
