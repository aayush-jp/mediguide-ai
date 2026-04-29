from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.routes import symptom, chat, report

app = FastAPI(
    title="MediGuide AI API",
    description=(
        "Clinical support assistant API — symptom checking, medical chatbot, "
        "and health report analysis. Not a substitute for professional medical advice."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptom.router)
app.include_router(chat.router)
app.include_router(report.router)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "running",
        "disclaimer": (
            "MediGuide AI is a clinical support tool, not a substitute for "
            "professional medical advice, diagnosis, or treatment."
        ),
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."},
    )
