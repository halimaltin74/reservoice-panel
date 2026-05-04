from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("", response_model=list[schemas.TemplateOut])
def list_templates(category: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Template)
    if category:
        q = q.filter(models.Template.category == category)
    return q.all()


@router.post("", response_model=schemas.TemplateOut, status_code=201)
def create_template(payload: schemas.TemplateCreate, db: Session = Depends(get_db)):
    t = models.Template(**payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{tid}", status_code=204)
def delete_template(tid: int, db: Session = Depends(get_db)):
    t = db.get(models.Template, tid)
    if not t:
        raise HTTPException(404)
    db.delete(t)
    db.commit()
