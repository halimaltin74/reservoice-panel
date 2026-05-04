from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


@router.get("", response_model=list[schemas.CampaignOut])
def list_campaigns(status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Campaign)
    if status:
        q = q.filter(models.Campaign.status == status)
    return q.order_by(models.Campaign.created_at.desc()).all()


@router.post("", response_model=schemas.CampaignOut, status_code=201)
def create_campaign(payload: schemas.CampaignCreate, db: Session = Depends(get_db)):
    c = models.Campaign(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.post("/{cid}/publish", response_model=schemas.CampaignOut)
def publish(cid: int, db: Session = Depends(get_db)):
    """Mock — kampanya 'sent' olarak işaretlenir."""
    c = db.get(models.Campaign, cid)
    if not c:
        raise HTTPException(404)
    c.status = "sent"
    c.sent_count = (c.sent_count or 0) + 100  # mock recipient count
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{cid}", status_code=204)
def delete_campaign(cid: int, db: Session = Depends(get_db)):
    c = db.get(models.Campaign, cid)
    if not c:
        raise HTTPException(404)
    db.delete(c)
    db.commit()
