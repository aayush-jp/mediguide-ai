from fastapi import UploadFile


ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp", "application/pdf"}
MAX_BYTES = 8 * 1024 * 1024


async def analyze_report_upload(file: UploadFile) -> dict:
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES:
        raise ValueError("Only PNG, JPEG, WebP, and PDF reports are supported.")

    data = await file.read()
    if len(data) > MAX_BYTES:
        raise ValueError("File is too large. Maximum allowed size is 8 MB.")

    return {
        "file_name": file.filename,
        "report_type": "Medical report or prescription",
        "extracted_values": [
            {"name": "Hemoglobin", "value": "13.5 g/dL", "status": "Normal"},
            {"name": "WBC", "value": "7,200 /uL", "status": "Normal"},
            {"name": "Glucose", "value": "Needs OCR provider integration", "status": "Review"},
        ],
        "summary": "Report uploaded and validated. Connect Tesseract, EasyOCR, or a vision model for production OCR extraction.",
        "risk_level": "Medium",
        "disclaimer": "Report interpretation is AI-assisted and must be reviewed by a licensed clinician.",
    }
