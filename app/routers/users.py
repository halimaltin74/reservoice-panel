from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.post("", response_model=schemas.UserOut, status_code=201)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=payload.email).first():
        raise HTTPException(409, "email already exists")
    u = models.User(**payload.model_dump())
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{uid}", status_code=204)
def delete_user(uid: int, db: Session = Depends(get_db)):
    u = db.get(models.User, uid)
    if not u:
        raise HTTPException(404)
    db.delete(u)
    db.commit()
