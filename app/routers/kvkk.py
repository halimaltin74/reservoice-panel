from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/kvkk", tags=["kvkk"])


@router.get("", response_model=list[schemas.KvkkConsentOut])
def list_consents(db: Session = Depends(get_db)):
    return db.query(models.KvkkConsent).order_by(models.KvkkConsent.signed_at.desc()).all()


@router.post("", response_model=schemas.KvkkConsentOut, status_code=201)
def create_consent(payload: schemas.KvkkConsentCreate, db: Session = Depends(get_db)):
    c = models.KvkkConsent(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{cid}", status_code=204)
def revoke_consent(cid: int, db: Session = Depends(get_db)):
    """KVKK uyarınca kayıt silme talebi."""
    c = db.get(models.KvkkConsent, cid)
    if not c:
        raise HTTPException(404)
    db.delete(c)
    db.commit()
