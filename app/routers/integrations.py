from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("", response_model=list[schemas.IntegrationOut])
def list_integrations(category: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Integration)
    if category:
        q = q.filter(models.Integration.category == category)
    return q.all()


@router.get("/{key}", response_model=schemas.IntegrationOut)
def get_integration(key: str, db: Session = Depends(get_db)):
    i = db.query(models.Integration).filter_by(key=key).first()
    if not i:
        raise HTTPException(404, "integration not found")
    return i


@router.patch("/{key}", response_model=schemas.IntegrationOut)
def update_integration(key: str, payload: schemas.IntegrationUpdate, db: Session = Depends(get_db)):
    i = db.query(models.Integration).filter_by(key=key).first()
    if not i:
        raise HTTPException(404, "integration not found")
    data = payload.model_dump(exclude_unset=True)
    if "enabled" in data:
        i.enabled = data["enabled"]
    if "config" in data:
        i.config = data["config"]
    db.commit()
    db.refresh(i)
    return i


@router.post("/{key}/test")
def test_integration(key: str, db: Session = Depends(get_db)):
    """Mock connection test — gerçek API çağrısı yapılmaz."""
    i = db.query(models.Integration).filter_by(key=key).first()
    if not i:
        raise HTTPException(404, "integration not found")
    return {
        "key": key,
        "ok": i.enabled,
        "message": (
            "Bağlantı testi simüle edildi (mock)."
            if i.enabled
            else "Entegrasyon kapalı — önce enabled=true yapın."
        ),
    }
