from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Users ──
class UserBase(ORMBase):
    name: str
    email: str
    role: str = "staff"


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int
    created_at: datetime


# ── Conversations ──
class ConversationBase(ORMBase):
    guest_name: str
    channel: str
    room_type: Optional[str] = None
    stay_dates: Optional[str] = None
    status: str = "active"
    automation_pct: int = 100
    last_message: Optional[str] = None
    tag: Optional[str] = None
    waiting_minutes: int = 0


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(ORMBase):
    status: Optional[str] = None
    automation_pct: Optional[int] = None
    last_message: Optional[str] = None
    tag: Optional[str] = None
    waiting_minutes: Optional[int] = None


class ConversationOut(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ── Messages ──
class MessageBase(ORMBase):
    sender: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageOut(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime


# ── Reservations ──
class ReservationBase(ORMBase):
    code: Optional[str] = None
    guest_name: str
    channel: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    room_type: Optional[str] = None
    total: Optional[float] = None
    status: str = "pending"
    review_reason: Optional[str] = None
    conversation_id: Optional[int] = None


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ORMBase):
    status: Optional[str] = None
    review_reason: Optional[str] = None


class ReservationOut(ReservationBase):
    id: int
    created_at: datetime


# ── Tickets ──
class TicketBase(ORMBase):
    code: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: str = "normal"
    status: str = "open"
    room: Optional[str] = None
    guest_name: Optional[str] = None
    assigned_to: Optional[str] = None
    conversation_id: Optional[int] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(ORMBase):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    description: Optional[str] = None


class TicketOut(TicketBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None


# ── Hotel info ──
class HotelInfoIn(ORMBase):
    section: str
    data: dict[str, Any] = {}


class HotelInfoOut(HotelInfoIn):
    id: int
    updated_at: datetime


# ── Room ──
class RoomBase(ORMBase):
    name: str
    capacity: int = 2
    size_m2: Optional[int] = None
    base_price: Optional[float] = None
    amenities: list[str] = []


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int


# ── Restaurant ──
class RestaurantBase(ORMBase):
    name: str
    cuisine: Optional[str] = None
    hours: Optional[str] = None
    dress_code: Optional[str] = None
    capacity: Optional[int] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantOut(RestaurantBase):
    id: int


# ── AI Rules ──
class AIRuleBase(ORMBase):
    name: str
    trigger: Optional[str] = None
    action: Optional[str] = None
    enabled: bool = True


class AIRuleCreate(AIRuleBase):
    pass


class AIRuleUpdate(ORMBase):
    name: Optional[str] = None
    trigger: Optional[str] = None
    action: Optional[str] = None
    enabled: Optional[bool] = None


class AIRuleOut(AIRuleBase):
    id: int
    created_at: datetime


# ── Templates ──
class TemplateBase(ORMBase):
    category: Optional[str] = None
    name: str
    content: str
    channel: str = "whatsapp"


class TemplateCreate(TemplateBase):
    pass


class TemplateOut(TemplateBase):
    id: int


# ── Integrations ──
class IntegrationBase(ORMBase):
    key: str
    label: str
    category: Optional[str] = None
    enabled: bool = False
    config: dict[str, Any] = {}
    docs_url: Optional[str] = None


class IntegrationUpdate(ORMBase):
    enabled: Optional[bool] = None
    config: Optional[dict[str, Any]] = None


class IntegrationOut(IntegrationBase):
    id: int
    updated_at: datetime


# ── Upsell ──
class UpsellOfferBase(ORMBase):
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    segment: Optional[str] = None
    status: str = "active"
    sent_count: int = 0
    accepted_count: int = 0


class UpsellOfferCreate(UpsellOfferBase):
    pass


class UpsellOfferUpdate(ORMBase):
    status: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class UpsellOfferOut(UpsellOfferBase):
    id: int


# ── Campaigns ──
class CampaignBase(ORMBase):
    name: str
    channel: str = "whatsapp"
    segment: Optional[str] = None
    message: Optional[str] = None
    status: str = "draft"
    scheduled_at: Optional[datetime] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignOut(CampaignBase):
    id: int
    sent_count: int
    created_at: datetime


# ── KVKK ──
class KvkkConsentBase(ORMBase):
    guest_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    consent_marketing: bool = False
    consent_data: bool = True
    source: Optional[str] = None


class KvkkConsentCreate(KvkkConsentBase):
    pass


class KvkkConsentOut(KvkkConsentBase):
    id: int
    signed_at: datetime


# ── AI Performance ──
class AIPerformanceOut(ORMBase):
    id: int
    date: str
    automation_pct: Optional[float] = None
    handled: int
    escalated: int
    csat: Optional[float] = None
    avg_response_sec: Optional[int] = None
