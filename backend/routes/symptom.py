from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.agents.medical_agent import run_symptom_analysis

router = APIRouter(prefix="/api/v1", tags=["Symptom Checker"])


class SymptomCheckRequest(BaseModel):
    symptoms: List[str] = Field(..., min_length=1, description="List of reported symptoms")
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    duration_days: Optional[int] = Field(None, ge=0, le=365)
    severity: Optional[int] = Field(None, ge=1, le=10)
    temperature_f: Optional[float] = Field(None, ge=95.0, le=110.0)
    existing_conditions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medicines: Optional[List[str]] = None


class ConditionResult(BaseModel):
    name: str
    confidence: int
    risk_level: str
    description: str
    when_to_see_doctor: List[str]
    home_care: List[str]
    typical_duration: str


class ReferralResult(BaseModel):
    referral_needed: bool
    urgency: str
    message: str
    referral_type: str


class SymptomCheckResponse(BaseModel):
    narrative: str
    risk_level: str
    risk_score: int
    risk_color: str
    is_emergency: bool
    emergency_triggers: List[str]
    possible_conditions: List[dict]
    referral: dict
    disclaimer: str


@router.post("/symptom-check", response_model=SymptomCheckResponse)
async def symptom_check(request: SymptomCheckRequest):
    """
    Analyze patient symptoms and return possible conditions with risk level and next steps.
    """
    try:
        result = await run_symptom_analysis(
            symptoms=request.symptoms,
            age=request.age,
            gender=request.gender,
            duration_days=request.duration_days,
            severity=request.severity,
            temperature_f=request.temperature_f,
            existing_conditions=request.existing_conditions,
            allergies=request.allergies,
            medicines=request.medicines,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
