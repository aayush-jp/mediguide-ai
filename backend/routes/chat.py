from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agents.medical_agent import run_chat_agent

router = APIRouter(prefix="/api/v1", tags=["Medical Chatbot"])


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str
    is_emergency: bool


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Medical chatbot — engage in a multi-turn conversation to assess symptoms.
    """
    try:
        history = [{"role": m.role, "content": m.content} for m in request.history]
        result = await run_chat_agent(
            message=request.message,
            history=history,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
