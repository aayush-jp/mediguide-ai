from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app import models

    Base.metadata.create_all(bind=engine)
    seed_doctors()


def seed_doctors() -> None:
    from app.models import Doctor

    doctors = [
        Doctor(
            id="D101",
            name="Dr. Meera Iyer",
            specialization="General Physician",
            location="Central Clinic",
            gender="Female",
            languages="English,Hindi,Tamil",
            working_days="0,1,2,3,4,5",
            working_start="09:00",
            working_end="17:00",
            appointment_duration_minutes=30,
        ),
        Doctor(
            id="D102",
            name="Dr. Arjun Sharma",
            specialization="General Physician",
            location="North Wing",
            gender="Male",
            languages="English,Hindi",
            working_days="0,1,2,3,4,5",
            working_start="10:00",
            working_end="19:00",
            appointment_duration_minutes=30,
        ),
        Doctor(
            id="D201",
            name="Dr. Kavya Rao",
            specialization="Cardiologist",
            location="Heart Care Center",
            gender="Female",
            languages="English,Hindi,Kannada",
            working_days="0,1,2,3,4",
            working_start="08:30",
            working_end="15:30",
            appointment_duration_minutes=30,
        ),
        Doctor(
            id="D301",
            name="Dr. Sameer Khan",
            specialization="Dermatologist",
            location="Central Clinic",
            gender="Male",
            languages="English,Hindi,Urdu",
            working_days="1,2,3,4,5",
            working_start="11:00",
            working_end="18:00",
            appointment_duration_minutes=30,
        ),
        Doctor(
            id="D401",
            name="Dr. Nisha Menon",
            specialization="Pediatrician",
            location="Children's Health Unit",
            gender="Female",
            languages="English,Hindi,Malayalam",
            working_days="0,1,2,3,4,5",
            working_start="09:30",
            working_end="16:30",
            appointment_duration_minutes=30,
        ),
    ]

    with SessionLocal() as db:
        for doctor in doctors:
            if db.get(Doctor, doctor.id) is None:
                db.add(doctor)
        db.commit()
