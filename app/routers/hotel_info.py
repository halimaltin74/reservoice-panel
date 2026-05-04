from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/hotel-info", tags=["hotel-info"])


@router.get("", response_model=list[schemas.HotelInfoOut])
def list_sections(db: Session = Depends(get_db)):
    return db.query(models.HotelInfo).all()


@router.get("/{section}", response_model=schemas.HotelInfoOut)
def get_section(section: str, db: Session = Depends(get_db)):
    info = db.query(models.HotelInfo).filter_by(section=section).first()
    if not info:
        raise HTTPException(404, "section not found")
    return info


@router.put("/{section}", response_model=schemas.HotelInfoOut)
def upsert_section(section: str, payload: schemas.HotelInfoIn, db: Session = Depends(get_db)):
    info = db.query(models.HotelInfo).filter_by(section=section).first()
    if info:
        info.data = payload.data
    else:
        info = models.HotelInfo(section=section, data=payload.data)
        db.add(info)
    db.commit()
    db.refresh(info)
    return info


# ── Rooms ──
rooms_router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@rooms_router.get("", response_model=list[schemas.RoomOut])
def list_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()


@rooms_router.post("", response_model=schemas.RoomOut, status_code=201)
def create_room(payload: schemas.RoomCreate, db: Session = Depends(get_db)):
    r = models.Room(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@rooms_router.delete("/{rid}", status_code=204)
def delete_room(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.Room, rid)
    if not r:
        raise HTTPException(404)
    db.delete(r)
    db.commit()


# ── Restaurants ──
restaurants_router = APIRouter(prefix="/api/restaurants", tags=["restaurants"])


@restaurants_router.get("", response_model=list[schemas.RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()


@restaurants_router.post("", response_model=schemas.RestaurantOut, status_code=201)
def create_restaurant(payload: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    r = models.Restaurant(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@restaurants_router.delete("/{rid}", status_code=204)
def delete_restaurant(rid: int, db: Session = Depends(get_db)):
    r = db.get(models.Restaurant, rid)
    if not r:
        raise HTTPException(404)
    db.delete(r)
    db.commit()
