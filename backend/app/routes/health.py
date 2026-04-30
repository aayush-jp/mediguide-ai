from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HealthHistory, User
from app.schemas import HealthHistoryCreate, HealthHistoryOut
from app.security import get_current_user

router = APIRouter(prefix="/api/health-history", tags=["Health History"])


@router.get("", response_model=list[HealthHistoryOut])
def list_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(HealthHistory)
        .filter(HealthHistory.user_id == current_user.id)
        .order_by(HealthHistory.created_at.desc())
        .all()
    )


@router.post("", response_model=HealthHistoryOut)
def save_history(payload: HealthHistoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = HealthHistory(user_id=current_user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
