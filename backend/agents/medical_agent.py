"""
MediGuide AI — Claude Medical Agent
Orchestrates the agentic loop: Claude calls medical tools, gathers data,
and synthesizes a safe, structured clinical support response.
"""

import json
import asyncio
from typing import Any, AsyncGenerator, Dict, List, Optional

import anthropic

from backend.config import settings
from backend.mcp_tools.tools import (
    AGENT_TOOLS,
    tool_check_emergency_flags,
    tool_analyze_symptoms,
    tool_calculate_risk,
    tool_interpret_lab_values,
    tool_get_medical_info,
    tool_doctor_referral_rule,
)

MEDICAL_SYSTEM_PROMPT = """You are MediGuide AI, a clinical support assistant — NOT a doctor or diagnostic tool.

## Your Purpose
Help users understand their symptoms, interpret health reports, and determine the appropriate next step. Always present information as: "Possible conditions + risk level + next safe step."

## Core Rules (NEVER violate these)
1. You cannot diagnose. Use language like "possible," "may suggest," "consistent with."
2. NEVER prescribe medications, dosages, or specific drug names.
3. NEVER replace professional medical advice.
4. ALWAYS end every response with the safety disclaimer.
5. For EMERGENCY symptoms: immediately tell the user to call emergency services.
6. For report analysis: interpret values, never confirm or deny a diagnosis.

## Emergency Red Flags — Auto-Escalate Immediately
If the user mentions any of these, STOP and tell them to call 911 / go to the ER:
- Chest pain or pressure
- Difficulty breathing / shortness of breath
- Fainting, loss of consciousness
- Seizures or convulsions
- Severe uncontrolled bleeding
- Sudden severe headache ("worst headache of my life")
- Sudden confusion, facial drooping, arm weakness, slurred speech (stroke signs)
- Throat swelling, anaphylaxis
- High fever in infant under 3 months
- Blood in vomit, blue lips, suspected poisoning/overdose

## Response Format
Always use the tool pipeline:
1. `check_emergency_flags` — FIRST, always check for emergencies
2. `analyze_symptoms` — get condition matches and base risk
3. `calculate_risk` — apply patient profile modifiers
4. `doctor_referral_rule` — determine referral urgency
5. `get_medical_info` — fetch home care / doctor guidance (optional, for top condition)

Then write a structured response:
```
**Possible Conditions**
[List with confidence notes and brief descriptions]

**Risk Level: [LOW / MEDIUM / HIGH / EMERGENCY]**
[Plain-language explanation of why]

**Recommended Action**
[What to do next — specific and actionable]

**Home Care Tips** (only for LOW risk)
[Bullet points]

**When to Escalate**
[Signs that would require immediate medical attention]
```

## Tone
- Empathetic, calm, clear
- Never alarming unless genuinely warranted
- Explain medical terms in plain language
- Ask one follow-up question at a time if information is missing

## Safety Disclaimer
End EVERY response with exactly:
---
⚕️ *MediGuide AI provides general health information only, not medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for personal medical guidance. In a medical emergency, call your local emergency number immediately.*"""


CHAT_SYSTEM_PROMPT = """You are MediGuide AI, a friendly clinical support chatbot.

## Rules
1. Ask one clarifying question at a time to gather symptoms naturally.
2. NEVER prescribe medications or dosages.
3. NEVER make a diagnosis — say "may suggest" or "could be consistent with."
4. Detect emergency keywords and immediately direct users to emergency services.
5. Keep responses concise and in plain language.
6. Use tools to analyze symptoms when you have enough information.

## Emergency Keywords — Immediate Escalation
If user mentions: chest pain, can't breathe, fainting, seizure, severe bleeding,
worst headache ever, stroke signs, throat swelling, unconscious — STOP and say:

"⚠️ This sounds like it could be a medical emergency. Please call 911 (or your local emergency number) immediately or go to the nearest emergency room. Do NOT drive yourself."

## Gathering Information Flow
When a user reports symptoms, gather:
1. What symptoms? (Ask about all present symptoms)
2. How long? (Duration in days)
3. How severe? (1–10 scale)
4. Temperature? (If fever-related)
5. Age and any existing medical conditions?

Once you have enough, use `analyze_symptoms` → `check_emergency_flags` → `doctor_referral_rule`.

## Disclaimer
End every substantive health response with:
---
⚕️ *This is general health information, not medical advice. Consult a healthcare professional for personal guidance.*"""


async def _execute_tool(name: str, tool_input: Dict[str, Any]) -> Any:
    """Dispatch a tool call to the appropriate Python function."""
    if name == "check_emergency_flags":
        return tool_check_emergency_flags(**tool_input)
    elif name == "analyze_symptoms":
        return tool_analyze_symptoms(**tool_input)
    elif name == "calculate_risk":
        return tool_calculate_risk(**tool_input)
    elif name == "doctor_referral_rule":
        return tool_doctor_referral_rule(**tool_input)
    elif name == "interpret_lab_values":
        return tool_interpret_lab_values(**tool_input)
    elif name == "get_medical_info":
        return tool_get_medical_info(**tool_input)
    else:
        return {"error": f"Unknown tool: {name}"}


async def run_symptom_analysis(
    symptoms: List[str],
    age: Optional[int],
    gender: Optional[str],
    duration_days: Optional[int],
    severity: Optional[int],
    temperature_f: Optional[float],
    existing_conditions: Optional[List[str]],
    allergies: Optional[List[str]],
    medicines: Optional[List[str]],
) -> Dict[str, Any]:
    """
    Run the full symptom-checker agent pipeline.
    Returns a structured result combining tool data + LLM narrative.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    # Build a detailed user message
    parts = [f"Patient symptoms: {', '.join(symptoms)}"]
    if age:
        parts.append(f"Age: {age}")
    if gender:
        parts.append(f"Gender: {gender}")
    if duration_days is not None:
        parts.append(f"Duration: {duration_days} day(s)")
    if severity is not None:
        parts.append(f"Severity: {severity}/10")
    if temperature_f:
        parts.append(f"Temperature: {temperature_f}°F")
    if existing_conditions:
        parts.append(f"Existing conditions: {', '.join(existing_conditions)}")
    if allergies:
        parts.append(f"Allergies: {', '.join(allergies)}")
    if medicines:
        parts.append(f"Current medications: {', '.join(medicines)}")

    user_message = "\n".join(parts)
    messages = [{"role": "user", "content": user_message}]

    # Agentic loop
    final_text = ""
    tool_results_data = {}

    while True:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=MEDICAL_SYSTEM_PROMPT,
            tools=AGENT_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await _execute_tool(block.name, block.input)
                    tool_results_data[block.name] = result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            break
        else:
            break

    # Extract structured data for the frontend
    risk_data = tool_results_data.get("calculate_risk", {})
    emergency_data = tool_results_data.get("check_emergency_flags", {})
    conditions_data = tool_results_data.get("analyze_symptoms", {})
    referral_data = tool_results_data.get("doctor_referral_rule", {})

    return {
        "narrative": final_text,
        "risk_level": risk_data.get("level") or emergency_data.get("level", "UNKNOWN"),
        "risk_score": risk_data.get("score", 0),
        "risk_color": risk_data.get("color", "gray"),
        "is_emergency": emergency_data.get("level") == "EMERGENCY",
        "emergency_triggers": emergency_data.get("triggers", []),
        "possible_conditions": conditions_data.get("possible_conditions", [])[:3],
        "referral": referral_data,
        "disclaimer": (
            "MediGuide AI provides general health information only, not medical advice, "
            "diagnosis, or treatment. Always consult a qualified healthcare professional."
        ),
    }


async def run_chat_agent(
    message: str,
    history: List[Dict[str, str]],
) -> Dict[str, Any]:
    """
    Run the conversational medical chatbot agent.
    Maintains conversation history for follow-up questions.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    messages = []
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    is_emergency = False
    final_text = ""

    while True:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=CHAT_SYSTEM_PROMPT,
            tools=AGENT_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await _execute_tool(block.name, block.input)
                    # Track emergency status
                    if block.name == "check_emergency_flags":
                        is_emergency = result.get("level") == "EMERGENCY"
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            break
        else:
            break

    return {
        "response": final_text,
        "is_emergency": is_emergency,
    }


async def run_report_analysis(
    extracted_values: Dict[str, float],
    raw_summary: str,
    report_type: str,
    gender: Optional[str],
    special_notes: List[str],
) -> Dict[str, Any]:
    """
    Run the report analysis agent — synthesizes OCR-extracted values
    into a patient-friendly summary using Claude.
    """
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    # Build context message
    context = f"""Report type: {report_type}
Raw content summary: {raw_summary}
Extracted values: {json.dumps(extracted_values)}
Special notes already flagged in report: {json.dumps(special_notes)}
Patient gender: {gender or 'not specified'}

Please interpret these results using the interpret_lab_values tool,
then write a clear patient-friendly summary explaining:
1. Which values are normal, low, or high
2. What the abnormal values might suggest (use careful, non-diagnostic language)
3. What the patient should discuss with their doctor
4. Any values that need urgent attention"""

    messages = [{"role": "user", "content": context}]

    final_text = ""
    interpreted_values = []

    while True:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=3000,
            system=MEDICAL_SYSTEM_PROMPT,
            tools=AGENT_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await _execute_tool(block.name, block.input)
                    if block.name == "interpret_lab_values":
                        interpreted_values = result
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            break
        else:
            break

    return {
        "narrative": final_text,
        "interpreted_values": interpreted_values,
        "report_type": report_type,
    }
