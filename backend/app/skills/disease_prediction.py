def predict_disease(symptoms: list[str], age: int | None = None, duration_days: int | None = None) -> dict:
    text = " ".join(symptoms).lower()
    predictions = []

    rules = [
        (["fever", "cough"], "Flu-like illness", 0.74),
        (["sore throat", "fever"], "Upper respiratory infection", 0.69),
        (["headache", "nausea"], "Migraine pattern", 0.62),
        (["stomach", "diarrhea"], "Gastroenteritis pattern", 0.66),
        (["fatigue", "weak"], "Nutritional, sleep, or infection-related fatigue", 0.54),
    ]

    for terms, label, score in rules:
        if all(term in text for term in terms):
            predictions.append({"label": label, "probability": score})

    if not predictions:
        predictions.append({"label": "Needs more data for reliable prediction", "probability": 0.38})

    return {
        "model": "rule-assisted ML placeholder",
        "predictions": predictions,
        "note": "Predictions are educational AI estimates and are never final diagnoses.",
    }
