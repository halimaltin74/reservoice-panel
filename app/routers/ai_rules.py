from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/ai-rules", tags=["ai-rules"])


@router.get("", response_model=list[schemas.AIRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(models.AIRule).order_by(models.AIRule.created_at.desc()).all()


@router.post("", response_model=schemas.AIRuleOut, status_code=201)
def create_rule(payload: schemas.AIRuleCreate, db: Session = Depends(get_db)):
    r = models.AIRule(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.patch("/{rid}", response_model=schemas.AIRuleOut)
def update_rule(rid: int, payload: schemas.AIRuleUpdate, db: Session = Depends(get_db)):
    r = db.get(models.AIRule, rid)
    if not r:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{rid}", status_code=204)
def delete_rule(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.AIRule, rid)
    if not r:
        raise HTTPException(404)
    db.delete(r)
    db.commit()
