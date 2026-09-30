from datetime import timedelta
from django.conf import settings
import pytest
from django.utils import timezone

from apps.bookings.models import Booking
from apps.payments import octo
from apps.payments.models import Payment


def payload(d, days=5):
    start = timezone.now() + timedelta(days=1)
    return {
        "car": d["car"].id, "start_at": start.isoformat(),
        "end_at": (start + timedelta(days=days)).isoformat(),
        "pickup_location": d["city"].id, "return_location": d["airport"].id,
        "extras": [{"code": "wifi", "qty": 1}],
        "customer_name": "Ali Valiyev", "phone": "+998901234567",
    }


def test_quote_uses_tier_and_fees(api, setup_data):
    r = api.post("/api/bookings/quote/", payload(setup_data), format="json")
    assert r.status_code == 200
    assert r.data["daily_price"] == 90_000      # 4–7 kunlik tarif
    assert r.data["rent_sum"] == 450_000
    assert r.data["total_sum"] == 450_000 + 100_000 + 200_000


@pytest.fixture
def created(api, setup_data, monkeypatch):
    monkeypatch.setattr(octo, "prepare_payment", lambda b: {
        "octo_payment_UUID": "uuid-1", "octo_pay_url": "http://pay/uuid-1"})
    r = api.post("/api/bookings/", payload(setup_data), format="json")
    assert r.status_code == 201, r.data
    return Booking.objects.get(id=r.data["booking_id"])


def notify(booking, status="succeeded", **over):
    unique_key = "mock_unique_key_for_testing"
    raw = f"{unique_key}uuid-1{status}"
    signature = __import__("hashlib").sha1(raw.encode()).hexdigest().upper()

    b = {
        "octo_payment_UUID": "uuid-1",
        "shop_transaction_id": str(booking.id),
        "status": status,
        "total_sum": booking.total_sum,
        "signature": signature,
        "hash_key": signature,
    }
    b.update(over)
    return b

def test_booking_created_pending(created):
    assert created.status == "pending"
    assert Payment.objects.get(booking=created).amount == created.total_sum


def test_double_booking_rejected(api, setup_data, created):
    assert api.post("/api/bookings/", payload(setup_data), format="json").status_code == 400


def test_webhook_paid_and_idempotent(api, created, monkeypatch):
    monkeypatch.setattr(
        octo,
        "verify_payment_status",
        lambda tx: {
            "octo_payment_UUID": "uuid-1",
            "status": "succeeded",
        },
    )

    for _ in range(2):
        assert api.post(
            "/api/payments/octo/notify/",
            notify(created),
            format="json",
        ).status_code == 200

    created.refresh_from_db()
    assert created.status == "paid"

def test_webhook_works_without_unique_key(api, created, monkeypatch):
    monkeypatch.setattr(settings, "OCTO_UNIQUE_KEY", "")
    monkeypatch.setattr(
        octo,
        "verify_payment_status",
        lambda tx: {
            "octo_payment_UUID": "uuid-1",
            "status": "succeeded",
        },
    )

    response = api.post(
        "/api/payments/octo/notify/",
        notify(created),
        format="json",
    )

    assert response.status_code == 200

    created.refresh_from_db()
    assert created.status == "paid"

def test_webhook_rejects_bad_signature_and_sum(api, created, monkeypatch):
    monkeypatch.setattr(settings, "OCTO_UNIQUE_KEY", "test_unique_key")
    monkeypatch.setattr(
        octo,
        "verify_payment_status",
        lambda tx: {
            "octo_payment_UUID": "uuid-1",
            "status": "succeeded",
        },
    )

    assert api.post(
        "/api/payments/octo/notify/",
        notify(created, signature="x"),
        format="json",
    ).status_code == 400

    assert api.post(
        "/api/payments/octo/notify/",
        notify(created, total_sum=1),
        format="json",
    ).status_code == 400

    created.refresh_from_db()
    assert created.status == "pending"

def test_canceled_payment_frees_car(api, setup_data, created, monkeypatch):
    monkeypatch.setattr(
        octo,
        "verify_payment_status",
        lambda tx: {
            "octo_payment_UUID": "uuid-1",
            "status": "canceled",
        },
    )

    assert api.post(
        "/api/payments/octo/notify/",
        notify(created, status="canceled"),
        format="json",
    ).status_code == 200

    r = api.get(
        "/api/cars/",
        {
            "start": created.start_at.isoformat(),
            "end": created.end_at.isoformat(),
        },
    )

    assert [c["id"] for c in r.data] == [setup_data["car"].id]