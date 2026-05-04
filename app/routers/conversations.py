from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("", response_model=list[schemas.ConversationOut])
def list_conversations(status: str | None = None, channel: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Conversation)
    if status:
        q = q.filter(models.Conversation.status == status)
    if channel:
        q = q.filter(models.Conversation.channel == channel)
    return q.order_by(models.Conversation.updated_at.desc()).all()


@router.get("/stats")
def conversation_stats(db: Session = Depends(get_db)):
    total = db.query(models.Conversation).count()
    takeover = db.query(models.Conversation).filter_by(status="takeover").count()
    active = db.query(models.Conversation).filter_by(status="active").count()
    done = db.query(models.Conversation).filter_by(status="done").count()
    avg_auto = db.query(models.Conversation).all()
    avg = round(sum(c.automation_pct for c in avg_auto) / max(len(avg_auto), 1))
    return {"total": total, "takeover": takeover, "active": active, "done": done, "automation_pct": avg}


@router.get("/{conv_id}", response_model=schemas.ConversationOut)
def get_conversation(conv_id: int, db: Session = Depends(get_db)):
    c = db.get(models.Conversation, conv_id)
    if not c:
        raise HTTPException(404, "conversation not found")
    return c


@router.post("", response_model=schemas.ConversationOut, status_code=201)
def create_conversation(payload: schemas.ConversationCreate, db: Session = Depends(get_db)):
    c = models.Conversation(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.patch("/{conv_id}", response_model=schemas.ConversationOut)
def update_conversation(conv_id: int, payload: schemas.ConversationUpdate, db: Session = Depends(get_db)):
    c = db.get(models.Conversation, conv_id)
    if not c:
        raise HTTPException(404, "conversation not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c


@router.post("/{conv_id}/takeover", response_model=schemas.ConversationOut)
def takeover(conv_id: int, db: Session = Depends(get_db)):
    c = db.get(models.Conversation, conv_id)
    if not c:
        raise HTTPException(404, "conversation not found")
    c.status = "takeover"
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{conv_id}", status_code=204)
def delete_conversation(conv_id: int, db: Session = Depends(get_db)):
    c = db.get(models.Conversation, conv_id)
    if not c:
        raise HTTPException(404, "conversation not found")
    db.delete(c)
    db.commit()


# ── Messages ──
@router.get("/{conv_id}/messages", response_model=list[schemas.MessageOut])
def list_messages(conv_id: int, db: Session = Depends(get_db)):
    if not db.get(models.Conversation, conv_id):
        raise HTTPException(404, "conversation not found")
    return (
        db.query(models.Message)
        .filter_by(conversation_id=conv_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )


@router.post("/{conv_id}/messages", response_model=schemas.MessageOut, status_code=201)
def add_message(conv_id: int, payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    c = db.get(models.Conversation, conv_id)
    if not c:
        raise HTTPException(404, "conversation not found")
    m = models.Message(conversation_id=conv_id, **payload.model_dump())
    c.last_message = payload.content
    c.updated_at = datetime.utcnow()
    db.add(m)
    db.commit()
    db.refresh(m)
    return m
