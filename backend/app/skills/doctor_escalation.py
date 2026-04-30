def escalation_advice(risk_level: str) -> dict:
    if risk_level == "Emergency":
        return {"escalate": True, "urgency": "Emergency", "message": "Call emergency services now."}
    if risk_level == "High":
        return {"escalate": True, "urgency": "Same day", "message": "Doctor review is recommended today."}
    if risk_level == "Medium":
        return {"escalate": True, "urgency": "If persistent", "message": "See a doctor if symptoms persist, worsen, or remain unclear."}
    return {"escalate": False, "urgency": "Monitor", "message": "Doctor visit is not automatically required unless symptoms persist or worsen."}
