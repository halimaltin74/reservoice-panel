from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


def _next_code(db: Session) -> str:
    n = db.query(models.Ticket).count() + 1
    return f"TKT-{n:03d}"


@router.get("", response_model=list[schemas.TicketOut])
def list_tickets(
    status: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Ticket)
    if status:
        q = q.filter(models.Ticket.status == status)
    if priority:
        q = q.filter(models.Ticket.priority == priority)
    if category:
        q = q.filter(models.Ticket.category == category)
    return q.order_by(models.Ticket.created_at.desc()).all()


@router.get("/stats")
def ticket_stats(db: Session = Depends(get_db)):
    return {
        "open": db.query(models.Ticket).filter_by(status="open").count(),
        "in_progress": db.query(models.Ticket).filter_by(status="in_progress").count(),
        "resolved": db.query(models.Ticket).filter_by(status="resolved").count(),
        "total": db.query(models.Ticket).count(),
    }


@router.get("/{tid}", response_model=schemas.TicketOut)
def get_ticket(tid: int, db: Session = Depends(get_db)):
    t = db.get(models.Ticket, tid)
    if not t:
        raise HTTPException(404)
    return t


@router.post("", response_model=schemas.TicketOut, status_code=201)
def create_ticket(payload: schemas.TicketCreate, db: Session = Depends(get_db)):
    t = models.Ticket(**payload.model_dump())
    if not t.code:
        t.code = _next_code(db)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.patch("/{tid}", response_model=schemas.TicketOut)
def update_ticket(tid: int, payload: schemas.TicketUpdate, db: Session = Depends(get_db)):
    t = db.get(models.Ticket, tid)
    if not t:
        raise HTTPException(404)
    data = payload.model_dump(exclude_unset=True)
    if data.get("status") == "resolved" and t.resolved_at is None:
        t.resolved_at = datetime.utcnow()
    for k, v in data.items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return t


@router.post("/{tid}/resolve", response_model=schemas.TicketOut)
def resolve(tid: int, db: Session = Depends(get_db)):
    t = db.get(models.Ticket, tid)
    if not t:
        raise HTTPException(404)
    t.status = "resolved"
    t.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{tid}", status_code=204)
def delete_ticket(tid: int, db: Session = Depends(get_db)):
    t = db.get(models.Ticket, tid)
    if not t:
        raise HTTPException(404)
    db.delete(t)
    db.commit()
