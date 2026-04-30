LANGUAGE_HINTS = {
    "Hindi": "Hindi response support enabled.",
    "Tamil": "Tamil response support enabled.",
    "Kannada": "Kannada response support enabled.",
    "Telugu": "Telugu response support enabled.",
    "Malayalam": "Malayalam response support enabled.",
}


def localize_response(text: str, language: str) -> str:
    if language == "English":
        return text
    return f"{LANGUAGE_HINTS.get(language, 'Multilingual support enabled')} {text}"
