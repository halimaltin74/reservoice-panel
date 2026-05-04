from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/reservations", tags=["reservations"])


@router.get("", response_model=list[schemas.ReservationOut])
def list_reservations(status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Reservation)
    if status:
        q = q.filter(models.Reservation.status == status)
    return q.order_by(models.Reservation.created_at.desc()).all()


@router.get("/stats")
def reservation_stats(db: Session = Depends(get_db)):
    return {
        "pending": db.query(models.Reservation).filter_by(status="pending").count(),
        "auto_approved": db.query(models.Reservation).filter_by(status="auto_approved").count(),
        "approved": db.query(models.Reservation).filter_by(status="approved").count(),
        "rejected": db.query(models.Reservation).filter_by(status="rejected").count(),
        "total": db.query(models.Reservation).count(),
    }


@router.get("/{rid}", response_model=schemas.ReservationOut)
def get_reservation(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.Reservation, rid)
    if not r:
        raise HTTPException(404)
    return r


@router.post("", response_model=schemas.ReservationOut, status_code=201)
def create_reservation(payload: schemas.ReservationCreate, db: Session = Depends(get_db)):
    r = models.Reservation(**payload.model_dump())
    if not r.code:
        r.code = f"AI-REZ-{int(datetime.utcnow().timestamp())}"
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.patch("/{rid}", response_model=schemas.ReservationOut)
def update_reservation(rid: int, payload: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    r = db.get(models.Reservation, rid)
    if not r:
        raise HTTPException(404)
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r


@router.post("/{rid}/approve", response_model=schemas.ReservationOut)
def approve(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.Reservation, rid)
    if not r:
        raise HTTPException(404)
    r.status = "approved"
    db.commit()
    db.refresh(r)
    return r


@router.post("/{rid}/reject", response_model=schemas.ReservationOut)
def reject(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.Reservation, rid)
    if not r:
        raise HTTPException(404)
    r.status = "rejected"
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{rid}", status_code=204)
def delete_reservation(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.Reservation, rid)
    if not r:
        raise HTTPException(404)
    db.delete(r)
    db.commit()
