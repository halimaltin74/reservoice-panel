from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/ai-performance", tags=["ai-performance"])


@router.get("", response_model=list[schemas.AIPerformanceOut])
def list_performance(db: Session = Depends(get_db)):
    return db.query(models.AIPerformance).order_by(models.AIPerformance.date.desc()).all()


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    rows = db.query(models.AIPerformance).all()
    if not rows:
        return {"automation_pct": 0, "csat": 0, "handled": 0, "escalated": 0, "avg_response_sec": 0}
    n = len(rows)
    return {
        "automation_pct": round(sum(r.automation_pct or 0 for r in rows) / n, 1),
        "csat": round(sum(r.csat or 0 for r in rows) / n, 2),
        "handled": sum(r.handled for r in rows),
        "escalated": sum(r.escalated for r in rows),
        "avg_response_sec": round(sum(r.avg_response_sec or 0 for r in rows) / n),
    }
