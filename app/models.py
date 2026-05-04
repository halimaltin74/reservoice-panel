from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="staff")  # admin | staff
    created_at = Column(DateTime, default=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    guest_name = Column(String, nullable=False)
    channel = Column(String, nullable=False)  # whatsapp | chat | phone | telegram
    room_type = Column(String)
    stay_dates = Column(String)
    status = Column(String, default="active")  # active | takeover | done
    automation_pct = Column(Integer, default=100)
    last_message = Column(Text)
    tag = Column(String)
    waiting_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"))
    sender = Column(String, nullable=False)  # guest | ai | staff
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    guest_name = Column(String, nullable=False)
    channel = Column(String)
    check_in = Column(String)
    check_out = Column(String)
    room_type = Column(String)
    total = Column(Float)
    status = Column(String, default="pending")  # pending | auto_approved | approved | rejected
    review_reason = Column(String)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)  # TKT-001
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # housekeeping, technical, food, climate, noise, internet, other
    priority = Column(String, default="normal")  # urgent | high | normal | low
    status = Column(String, default="open")  # open | in_progress | resolved
    room = Column(String)
    guest_name = Column(String)
    assigned_to = Column(String)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class HotelInfo(Base):
    __tablename__ = "hotel_info"
    id = Column(Integer, primary_key=True)
    section = Column(String, unique=True, nullable=False)  # genel, checkin, odalar, havuz, ...
    data = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, default=2)
    size_m2 = Column(Integer)
    base_price = Column(Float)
    amenities = Column(JSON, default=list)


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cuisine = Column(String)
    hours = Column(String)
    dress_code = Column(String)
    capacity = Column(Integer)


class AIRule(Base):
    __tablename__ = "ai_rules"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    trigger = Column(String)
    action = Column(Text)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True)
    category = Column(String)  # rezervasyon, checkin, upsell, sikayet
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    channel = Column(String, default="whatsapp")  # whatsapp | sms | email | chat


class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)  # opera, mews, cloudbeds, ...
    label = Column(String, nullable=False)
    category = Column(String)  # pms | messaging | payment | sms
    enabled = Column(Boolean, default=False)
    config = Column(JSON, default=dict)
    docs_url = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UpsellOffer(Base):
    __tablename__ = "upsell_offers"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float)
    segment = Column(String)  # honeymoon, business, family, ...
    status = Column(String, default="active")  # active | paused | dismissed
    sent_count = Column(Integer, default=0)
    accepted_count = Column(Integer, default=0)


class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    channel = Column(String, default="whatsapp")
    segment = Column(String)
    message = Column(Text)
    status = Column(String, default="draft")  # draft | scheduled | sent
    scheduled_at = Column(DateTime, nullable=True)
    sent_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class KvkkConsent(Base):
    __tablename__ = "kvkk_consents"
    id = Column(Integer, primary_key=True)
    guest_name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    consent_marketing = Column(Boolean, default=False)
    consent_data = Column(Boolean, default=True)
    signed_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String)  # whatsapp, web, paper


class AIPerformance(Base):
    __tablename__ = "ai_performance"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    automation_pct = Column(Float)
    handled = Column(Integer, default=0)
    escalated = Column(Integer, default=0)
    csat = Column(Float)
    avg_response_sec = Column(Integer)
