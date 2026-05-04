"""Mock veri yükleyici — `python -m app.seed` ile çalıştır."""
from datetime import datetime, timedelta

from .database import Base, SessionLocal, engine
from . import models


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed_users(db):
    db.add_all([
        models.User(name="Halim Emiraltin", email="halim@reservoice.com", role="admin"),
        models.User(name="Otel Personeli", email="staff@reservoice.com", role="staff"),
    ])


def seed_conversations(db):
    convs = [
        models.Conversation(
            guest_name="Sarah Johnson", channel="chat", room_type="Suite",
            stay_dates="10–13 Tem", status="takeover", automation_pct=0,
            last_message='👋 "Bir yetkiliyle konuşmak istiyorum"',
            tag="Devralma", waiting_minutes=0,
        ),
        models.Conversation(
            guest_name="Mehmet Yılmaz", channel="whatsapp", room_type="Deluxe Room",
            stay_dates="7–12 Tem", status="takeover", automation_pct=0,
            last_message='👋 "Lütfen gerçek bir kişiyle bağlayın"',
            tag="Devralma", waiting_minutes=3,
        ),
        models.Conversation(
            guest_name="Anna Müller", channel="whatsapp", room_type="Standard Room",
            stay_dates="5–8 Tem", status="takeover", automation_pct=0,
            last_message='👋 "insan" anahtar kelimesi tetiklendi',
            tag="Devralma", waiting_minutes=7,
        ),
        models.Conversation(
            guest_name="Halim Emiraltin", channel="whatsapp", room_type="Family Room",
            stay_dates="14–16 Tem", status="active", automation_pct=92,
            last_message="Ödeme linki gönderildi",
            tag="Rezervasyon",
        ),
        models.Conversation(
            guest_name="Ahmed Al-Rashid", channel="telegram", room_type="Deluxe Room",
            stay_dates="20–25 Tem", status="done", automation_pct=100,
            last_message="Rezervasyon onaylandı",
            tag="Tamamlandı",
        ),
    ]
    db.add_all(convs)
    db.flush()

    # Halim'in (id=4) konuşma mesajları
    halim = convs[3]
    db.add_all([
        models.Message(conversation_id=halim.id, sender="guest",
                       content="Merhaba, 14-16 Temmuz için iki kişilik aile odası var mı?"),
        models.Message(conversation_id=halim.id, sender="ai",
                       content="Merhaba Halim Bey, evet Family Room müsait. Toplam 600₺. Onaylıyor musunuz?"),
        models.Message(conversation_id=halim.id, sender="guest", content="Evet, onaylıyorum."),
        models.Message(conversation_id=halim.id, sender="ai",
                       content="Harika, ödeme linki gönderildi. İyi günler dilerim 🌸"),
    ])


def seed_reservations(db):
    db.add_all([
        models.Reservation(
            code="AI-REZ-8MOYCHEM", guest_name="Halim Emiraltin", channel="whatsapp",
            check_in="2026-07-14", check_out="2026-07-16",
            room_type="Deluxe Room", total=900.0, status="pending",
            review_reason="Fiyat otomatik onay limitini aşıyor",
        ),
        models.Reservation(
            code="AI-REZ-S6N0EMP", guest_name="Hallim Emir Altın", channel="whatsapp",
            check_in="2026-07-07", check_out="2026-07-09",
            room_type="Family Room", total=600.0, status="auto_approved",
        ),
        models.Reservation(
            code="AI-REZ-K2T9PLM", guest_name="Sarah Johnson", channel="chat",
            check_in="2026-07-10", check_out="2026-07-13",
            room_type="Suite", total=2400.0, status="pending",
            review_reason="VIP misafir, manuel kontrol",
        ),
    ])


def seed_tickets(db):
    db.add_all([
        models.Ticket(
            code="TKT-001", title="Odada böcek / örümcek var",
            description="Odamın banyosunda büyük bir örümcek var, çok korkuttum. Lütfen acil olarak birisini gönderin.",
            category="housekeeping", priority="urgent", status="open",
            room="214", guest_name="Sarah Johnson",
        ),
        models.Ticket(
            code="TKT-002", title="Yastık eksik, battaniye yırtık",
            description="Odamda yastık sadece 1 tane var, 2 kişiyiz. Ayrıca battaniyenin bir köşesi yırtık, değiştirilmesini istiyorum.",
            category="housekeeping", priority="high", status="open",
            room="307", guest_name="Mehmet Yılmaz",
        ),
        models.Ticket(
            code="TKT-003", title="Klima çalışmıyor",
            description="Odanın klimasi soğutmuyor.",
            category="climate", priority="high", status="in_progress",
            room="412", guest_name="Anna Müller", assigned_to="Teknik Servis",
        ),
        models.Ticket(
            code="TKT-004", title="Wi-Fi bağlantı sorunu",
            description="Odadan internete bağlanamıyorum.",
            category="internet", priority="normal", status="resolved",
            room="105", guest_name="Halim Emiraltin",
            resolved_at=datetime.utcnow() - timedelta(hours=2),
        ),
    ])


def seed_hotel_info(db):
    sections = [
        ("genel", {
            "name": "İbis Styles Merter",
            "stars": 4,
            "address": "Merter, İstanbul",
            "phone": "+90 212 555 0000",
            "email": "info@ibis-merter.com",
            "languages": ["TR", "EN", "AR", "RU"],
        }),
        ("checkin", {"check_in": "14:00", "check_out": "12:00", "early_checkin_fee": 250}),
        ("odalar", {
            "total_rooms": 168,
            "types": ["Standard", "Deluxe", "Family", "Suite"],
        }),
        ("havuz", {"has_pool": True, "indoor": True, "outdoor": False, "hours": "07:00-22:00"}),
        ("yiyecek", {"breakfast_included": True, "all_inclusive": False}),
        ("spa", {"has_spa": True, "hammam": True, "sauna": True}),
        ("plaj", {"has_beach": False}),
        ("ulasim", {
            "airport_shuttle": True,
            "shuttle_fee": 350,
            "valet_parking": True,
        }),
        ("toplanti", {"meeting_rooms": 3, "max_capacity": 200}),
        ("ozel", {"pet_friendly": False, "smoking_rooms": False}),
        ("politika", {"cancellation_hours": 24, "deposit_required": True}),
        ("wifi", {"free": True, "ssid": "IbisGuest", "password": "ibis2026"}),
        ("dil", {"primary": "tr", "supported": ["tr", "en", "ar", "ru"]}),
    ]
    for key, data in sections:
        db.add(models.HotelInfo(section=key, data=data))


def seed_rooms(db):
    db.add_all([
        models.Room(name="Standard Room", capacity=2, size_m2=22, base_price=1800,
                    amenities=["Klima", "TV", "Wi-Fi", "Mini bar"]),
        models.Room(name="Deluxe Room", capacity=2, size_m2=28, base_price=2400,
                    amenities=["Klima", "TV", "Wi-Fi", "Mini bar", "Çay/kahve"]),
        models.Room(name="Family Room", capacity=4, size_m2=36, base_price=3000,
                    amenities=["Klima", "TV", "Wi-Fi", "Mini bar", "Bağlantı kapısı"]),
        models.Room(name="Suite", capacity=2, size_m2=48, base_price=4800,
                    amenities=["Klima", "TV", "Wi-Fi", "Mini bar", "Oturma odası", "Jakuzi"]),
    ])


def seed_restaurants(db):
    db.add_all([
        models.Restaurant(name="Lobby Restaurant", cuisine="Akdeniz",
                          hours="07:00-23:00", capacity=120),
        models.Restaurant(name="Sky Bar", cuisine="Bar/Snack",
                          hours="17:00-01:00", dress_code="Smart casual", capacity=60),
    ])


def seed_ai_rules(db):
    db.add_all([
        models.AIRule(name='"İnsan" anahtar kelimesi devralma',
                      trigger='message contains "insan" OR "yetkili"',
                      action='Konuşmayı durakla, personeli bilgilendir', enabled=True),
        models.AIRule(name="Fiyat limiti otomatik onay",
                      trigger="reservation.total <= 1500",
                      action="Otomatik onayla", enabled=True),
        models.AIRule(name="Şikayet → bilet oluştur",
                      trigger='intent == "complaint"',
                      action="Otomatik bilet oluştur ve kategori ata", enabled=True),
        models.AIRule(name="VIP misafir manuel kontrol",
                      trigger="guest.tags contains 'VIP'",
                      action="Manuel onay gerektir", enabled=True),
    ])


def seed_templates(db):
    db.add_all([
        models.Template(category="rezervasyon", name="Rezervasyon onayı",
                        content="Sayın {ad}, {checkin}-{checkout} tarihleri için {oda} rezervasyonunuz oluşturuldu. Toplam: {tutar}₺",
                        channel="whatsapp"),
        models.Template(category="checkin", name="Check-in hatırlatma",
                        content="Sayın {ad}, yarın saat 14:00'ten itibaren check-in yapabilirsiniz. Sizleri ağırlamak için sabırsızlanıyoruz.",
                        channel="whatsapp"),
        models.Template(category="upsell", name="Oda upgrade önerisi",
                        content="Sayın {ad}, sadece {fark}₺ fark ile {ust_oda}'ya geçebilirsiniz. İlgilenir misiniz?",
                        channel="whatsapp"),
        models.Template(category="sikayet", name="Şikayet alındı",
                        content="Sayın {ad}, geri bildiriminiz için teşekkürler. Konunuz {bilet} numaralı talep olarak kayıt altına alındı.",
                        channel="whatsapp"),
    ])


def seed_integrations(db):
    items = [
        # PMS
        ("opera", "Oracle OPERA Cloud", "pms", "https://docs.oracle.com/en/industries/hospitality/opera-cloud/"),
        ("mews", "Mews", "pms", "https://mews-systems.gitbook.io/connector-api/"),
        ("cloudbeds", "Cloudbeds", "pms", "https://hotels.cloudbeds.com/api/v1.1/"),
        ("beds24", "Beds24", "pms", "https://beds24.com/api/v2"),
        ("hotelrunner", "HotelRunner", "pms", "https://developer.hotelrunner.com/"),
        # Messaging
        ("whatsapp", "WhatsApp Business", "messaging", "https://developers.facebook.com/docs/whatsapp/"),
        ("telegram", "Telegram Bot", "messaging", "https://core.telegram.org/bots/api"),
        ("instagram", "Instagram DM", "messaging", "https://developers.facebook.com/docs/messenger-platform/instagram/"),
        # Payment
        ("iyzico", "iyzico", "payment", "https://dev.iyzipay.com/"),
        ("paytr", "PayTR", "payment", "https://dev.paytr.com/"),
        # SMS
        ("netgsm", "NetGSM", "sms", "https://www.netgsm.com.tr/dokuman/"),
        ("twilio", "Twilio", "sms", "https://www.twilio.com/docs"),
    ]
    for key, label, category, docs in items:
        db.add(models.Integration(
            key=key, label=label, category=category, docs_url=docs,
            enabled=(key == "whatsapp"),  # demo: whatsapp aktif
            config={},
        ))


def seed_upsell(db):
    db.add_all([
        models.UpsellOffer(title="Suite Yükseltme",
                           description="2400₺ farkla Suite'e geçin",
                           price=2400, segment="honeymoon", status="active",
                           sent_count=12, accepted_count=4),
        models.UpsellOffer(title="Geç Çıkış (16:00)",
                           description="Saat 16'ya kadar geç çıkış — 250₺",
                           price=250, segment="business", status="active",
                           sent_count=28, accepted_count=18),
        models.UpsellOffer(title="Romantik Akşam Yemeği",
                           description="Sky Bar'da çift kişilik akşam yemeği",
                           price=1800, segment="honeymoon", status="active",
                           sent_count=8, accepted_count=3),
        models.UpsellOffer(title="Aile Paketi (havuz + kahvaltı)",
                           description="Çocuklara özel havuz erişimi + ailecek brunch",
                           price=950, segment="family", status="paused",
                           sent_count=4, accepted_count=1),
    ])


def seed_campaigns(db):
    db.add_all([
        models.Campaign(name="Yaz erken rezervasyon", channel="whatsapp",
                        segment="all", message="Yaz tatili erken rezervasyonda %20 indirim — son 7 gün!",
                        status="sent", sent_count=850),
        models.Campaign(name="Bayram özel", channel="sms",
                        segment="repeat", message="Sadık misafirlerimize özel bayram fırsatı.",
                        status="draft"),
    ])


def seed_kvkk(db):
    db.add_all([
        models.KvkkConsent(guest_name="Halim Emiraltin", phone="+905551112233",
                           email="halim@reservoice.com",
                           consent_marketing=True, consent_data=True, source="whatsapp"),
        models.KvkkConsent(guest_name="Sarah Johnson", phone="+905554445566",
                           consent_marketing=False, consent_data=True, source="web"),
        models.KvkkConsent(guest_name="Mehmet Yılmaz", phone="+905557778899",
                           consent_marketing=True, consent_data=True, source="whatsapp"),
    ])


def seed_ai_performance(db):
    base = datetime(2026, 5, 1)
    for i in range(7):
        d = base + timedelta(days=i)
        db.add(models.AIPerformance(
            date=d.strftime("%Y-%m-%d"),
            automation_pct=78 + i * 1.5,
            handled=120 + i * 8,
            escalated=14 - i,
            csat=4.3 + (i * 0.05),
            avg_response_sec=42 - i * 2,
        ))


def main():
    print("⏳  Reset & seed başlıyor...")
    reset_db()
    db = SessionLocal()
    try:
        seed_users(db)
        seed_conversations(db)
        seed_reservations(db)
        seed_tickets(db)
        seed_hotel_info(db)
        seed_rooms(db)
        seed_restaurants(db)
        seed_ai_rules(db)
        seed_templates(db)
        seed_integrations(db)
        seed_upsell(db)
        seed_campaigns(db)
        seed_kvkk(db)
        seed_ai_performance(db)
        db.commit()
        print("✅  Mock veri yüklendi.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
