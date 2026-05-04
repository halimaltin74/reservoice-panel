from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import (
    ai_performance,
    ai_rules,
    campaigns,
    conversations,
    hotel_info,
    integrations,
    kvkk,
    reservations,
    templates,
    tickets,
    upsell,
    users,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Reservoice Panel API",
    description="Hotel AI yönetim paneli backend'i — FastAPI + SQLite (mock entegrasyonlar).",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"ok": True, "service": "reservoice-panel"}


app.include_router(conversations.router)
app.include_router(reservations.router)
app.include_router(tickets.router)
app.include_router(hotel_info.router)
app.include_router(hotel_info.rooms_router)
app.include_router(hotel_info.restaurants_router)
app.include_router(ai_rules.router)
app.include_router(templates.router)
app.include_router(integrations.router)
app.include_router(upsell.router)
app.include_router(campaigns.router)
app.include_router(kvkk.router)
app.include_router(users.router)
app.include_router(ai_performance.router)


# Static panel
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
