from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    history: Mapped[list["HealthHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class HealthHistory(Base):
    __tablename__ = "health_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(40), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="history")


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    specialization: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(40), nullable=False)
    languages: Mapped[str] = mapped_column(String(255), nullable=False)
    working_days: Mapped[str] = mapped_column(String(80), nullable=False, default="0,1,2,3,4")
    working_start: Mapped[str] = mapped_column(String(5), nullable=False, default="09:00")
    working_end: Mapped[str] = mapped_column(String(5), nullable=False, default="17:00")
    appointment_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=30)

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    doctor_id: Mapped[str] = mapped_column(ForeignKey("doctors.id"), nullable=False, index=True)
    specialization: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    urgency_level: Mapped[str] = mapped_column(String(24), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="confirmed")
    constraints: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    reasoning: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="appointments")
    doctor: Mapped[Doctor] = relationship(back_populates="appointments")
