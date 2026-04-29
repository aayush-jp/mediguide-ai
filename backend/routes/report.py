import base64
import io
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from backend.mcp_tools.tools import tool_analyze_report_image
from backend.agents.medical_agent import run_report_analysis

router = APIRouter(prefix="/api/v1", tags=["Report Analysis"])

ALLOWED_TYPES = {
    "image/jpeg": "image/jpeg",
    "image/png": "image/png",
    "image/webp": "image/webp",
    "image/gif": "image/gif",
}

MAX_FILE_SIZE_MB = 10


class ReportAnalysisResponse(BaseModel):
    narrative: str
    interpreted_values: list
    report_type: str


@router.post("/report-analyze", response_model=ReportAnalysisResponse)
async def analyze_report(
    file: UploadFile = File(..., description="Medical report image or PDF"),
    gender: Optional[str] = Form(None),
):
    """
    Upload a medical report image and receive an interpreted summary.
    Supports JPEG, PNG, WebP image formats.
    """
    # Validate file type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES and not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {content_type}. Please upload an image (JPEG, PNG, WebP).",
        )

    # Read and validate file size
    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed is {MAX_FILE_SIZE_MB} MB.",
        )

    # Encode to base64 for Claude Vision
    image_b64 = base64.standard_b64encode(file_bytes).decode("utf-8")
    media_type = ALLOWED_TYPES.get(content_type, "image/jpeg")

    try:
        # Step 1: Extract values via Claude Vision OCR
        extracted = await tool_analyze_report_image(
            image_data=image_b64,
            media_type=media_type,
            gender=gender,
        )

        # Step 2: Run the report analysis agent for narrative
        result = await run_report_analysis(
            extracted_values={
                item["test"]: item["value"]
                for item in extracted.get("interpreted_values", [])
            },
            raw_summary=extracted.get("raw_summary", ""),
            report_type=extracted.get("report_type", "Medical Report"),
            gender=gender,
            special_notes=extracted.get("special_notes", []),
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report analysis failed: {str(e)}")
