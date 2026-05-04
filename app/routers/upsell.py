from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/upsell", tags=["upsell"])


@router.get("", response_model=list[schemas.UpsellOfferOut])
def list_offers(status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.UpsellOffer)
    if status:
        q = q.filter(models.UpsellOffer.status == status)
    return q.all()


@router.post("", response_model=schemas.UpsellOfferOut, status_code=201)
def create_offer(payload: schemas.UpsellOfferCreate, db: Session = Depends(get_db)):
    o = models.UpsellOffer(**payload.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o


@router.patch("/{oid}", response_model=schemas.UpsellOfferOut)
def update_offer(oid: int, payload: schemas.UpsellOfferUpdate, db: Session = Depends(get_db)):
    o = db.get(models.UpsellOffer, oid)
    if not o:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(o, k, v)
    db.commit()
    db.refresh(o)
    return o


@router.post("/{oid}/send")
def send_offer(oid: int, db: Session = Depends(get_db)):
    """Mock send — gerçek mesaj gönderilmez."""
    o = db.get(models.UpsellOffer, oid)
    if not o:
        raise HTTPException(404)
    o.sent_count += 1
    db.commit()
    return {"id": oid, "sent_count": o.sent_count, "ok": True}


@router.post("/{oid}/dismiss", response_model=schemas.UpsellOfferOut)
def dismiss(oid: int, db: Session = Depends(get_db)):
    o = db.get(models.UpsellOffer, oid)
    if not o:
        raise HTTPException(404)
    o.status = "dismissed"
    db.commit()
    db.refresh(o)
    return o


@router.delete("/{oid}", status_code=204)
def delete_offer(oid: int, db: Session = Depends(get_db)):
    o = db.get(models.UpsellOffer, oid)
    if not o:
        raise HTTPException(404)
    db.delete(o)
    db.commit()
