# Reservoice Panel

Hotel AI yönetim paneli — FastAPI + SQLite backend ile statik HTML frontend.

İbis Styles Merter demo verisiyle önyüklenmiş. 13 sayfa: Konuşmalar, Rezervasyonlar, Şikayetler, Otel Bilgileri, AI Öğrenme, AI Performansı, Entegrasyonlar, Upsell, AI Kuralları, Şablonlar, Toplu Mesaj, KVKK, Ayarlar.

## Hızlı başlangıç

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed              # SQLite'a mock veri yükle
uvicorn app.main:app --reload
```

Panel: http://localhost:8000/
API dokümantasyonu: http://localhost:8000/docs

## Yapı

```
app/
  main.py            # FastAPI app, static mount
  database.py        # SQLAlchemy engine + session
  models.py          # SQLAlchemy modelleri
  schemas.py         # Pydantic şemaları
  seed.py            # Mock veri yükleyici
  routers/           # CRUD endpoint'leri
    conversations.py
    reservations.py
    tickets.py
    hotel_info.py
    ai_rules.py
    templates.py
    integrations.py
    upsell.py
    campaigns.py
    kvkk.py
    users.py
  static/
    index.html       # Panel UI
    api.js           # Frontend → backend bağlantı katmanı
```

## Notlar

- Tüm dış servis entegrasyonları (PMS'ler, ödeme, mesajlaşma) **şimdilik mock** — config saklanır ama gerçek API çağrısı yapılmaz.
- Auth basit: `X-User-Role: admin|staff` header'ı ile rol simüle edilir.
- Veritabanı: `reservoice.db` (gitignore'da).
