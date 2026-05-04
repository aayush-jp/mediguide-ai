MCP_TOOLS = [
    "Symptom Analysis Skill",
    "Disease Prediction Skill",
    "OCR Report Skill",
    "Medical Safety Skill",
    "Risk Triage Skill",
    "Multilingual Response Skill",
    "Voice Transcription Skill",
    "Doctor Escalation Skill",
    "Patient Preference Skill",
    "Schedule Retrieval Tool",
    "Availability Analysis Skill",
    "Appointment Optimization Skill",
    "Appointment Conflict Resolution Skill",
    "Appointment Booking Tool",
]


def list_mcp_tools() -> dict:
    return {
        "server": "MediGuide AI MCP Server",
        "status": "ready",
        "tools": MCP_TOOLS,
    }
