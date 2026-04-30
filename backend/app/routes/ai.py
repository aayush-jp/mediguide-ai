from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.agent.controller import medical_agent
from app.mcp.server import list_mcp_tools
from app.models import User
from app.schemas import ChatRequest, DiseasePredictionRequest, RiskRequest, SymptomRequest
from app.security import get_current_user
from app.skills.ocr_report import analyze_report_upload
from app.skills.risk_triage import calculate_risk
from app.skills.voice_transcription import transcribe_voice_stub

router = APIRouter(prefix="/api/ai", tags=["Protected AI Tools"])


@router.get("/mcp-tools")
def mcp_tools(_: User = Depends(get_current_user)):
    return list_mcp_tools()


@router.post("/symptom-analysis")
def symptom_analysis(payload: SymptomRequest, _: User = Depends(get_current_user)):
    return medical_agent.run_symptom_pipeline(
        payload.symptoms,
        payload.age,
        payload.duration_days,
        payload.severity,
        payload.language,
    )


@router.post("/disease-prediction")
def disease_prediction(payload: DiseasePredictionRequest, _: User = Depends(get_current_user)):
    return medical_agent.run_prediction(payload.symptoms, payload.age, payload.duration_days)


@router.post("/chat")
def chatbot(payload: ChatRequest, _: User = Depends(get_current_user)):
    return medical_agent.run_chat(payload.message, payload.language)


@router.post("/report-ocr")
async def report_ocr(file: UploadFile = File(...), _: User = Depends(get_current_user)):
    try:
        return await analyze_report_upload(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/risk-score")
def risk_score(payload: RiskRequest, _: User = Depends(get_current_user)):
    return calculate_risk(payload.symptoms, payload.severity, payload.duration_days, payload.age)


@router.post("/voice-transcription")
def voice_transcription(_: User = Depends(get_current_user)):
    return transcribe_voice_stub()
