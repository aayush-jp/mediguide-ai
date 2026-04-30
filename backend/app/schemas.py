from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class UserPublic(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class SignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValueError("Enter a valid email address.")
        return email


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return value.strip().lower()


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class SymptomRequest(BaseModel):
    symptoms: list[str] = Field(min_length=1)
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = None
    duration_days: int | None = Field(default=None, ge=0, le=365)
    severity: int | None = Field(default=None, ge=1, le=10)
    language: str = "English"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: str = "English"


class DiseasePredictionRequest(BaseModel):
    symptoms: list[str] = Field(min_length=1)
    age: int | None = Field(default=None, ge=0, le=120)
    duration_days: int | None = Field(default=None, ge=0, le=365)


class RiskRequest(BaseModel):
    symptoms: list[str] = Field(default_factory=list)
    severity: int = Field(ge=1, le=10)
    duration_days: int = Field(ge=0, le=365)
    age: int | None = Field(default=None, ge=0, le=120)


class HealthHistoryCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    category: str = Field(min_length=2, max_length=80)
    risk_level: Literal["Low", "Medium", "High", "Emergency"]
    risk_score: int = Field(ge=0, le=100)
    summary: str = Field(min_length=2, max_length=4000)


class HealthHistoryOut(HealthHistoryCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
