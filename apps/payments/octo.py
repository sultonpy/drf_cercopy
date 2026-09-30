"""
Octo klienti. Mock va live'da BIR XIL kod: faqat OCTO_BASE_URL o'zgaradi.
DIQQAT: live'ga o'tishdan oldin maydon nomlari va imzo algoritmini
https://help.octo.uz hujjati bilan solishtiring.
"""
import hashlib
import hmac
import requests
from django.conf import settings
from django.utils import timezone


class OctoError(Exception):
    pass


def make_signature(octo_uuid: str, shop_transaction_id: str) -> str:
    raw = f"{settings.OCTO_SECRET}{shop_transaction_id}{octo_uuid}"
    return hashlib.sha1(raw.encode()).hexdigest().upper()


def prepare_payment(booking) -> dict:
    payload = {
        "octo_shop_id": settings.OCTO_SHOP_ID,
        "octo_secret": settings.OCTO_SECRET,
        "shop_transaction_id": str(booking.id),
        "auto_capture": True,
        "test": settings.OCTO_TEST,        "init_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_sum": booking.total_sum,
        "currency": "UZS",
        "description": f"Bron: {booking.car.name}, {booking.days} kun",
        "user_data": {"user_id": booking.phone, "phone": booking.phone, "email": booking.email},
        "return_url": f"{settings.PUBLIC_URL}/#/payment/{booking.id}",
        "notify_url": f"{settings.NOTIFY_BASE_URL}/api/payments/octo/notify/",
        "language": "uz",
        "ttl": settings.BOOKING_HOLD_MINUTES,
    }
    r = requests.post(f"{settings.OCTO_BASE_URL}/prepare_payment", json=payload, timeout=15)
    r.raise_for_status()
    body = r.json()
    if body.get("error") != 0:
        raise OctoError(body.get("errMessage", "Octo xatosi"))
    return body["data"]  # octo_payment_UUID, octo_pay_url

def verify_payment_status(shop_transaction_id: str) -> dict:
    payload = {
        "octo_shop_id": settings.OCTO_SHOP_ID,
        "octo_secret": settings.OCTO_SECRET,
        "shop_transaction_id": shop_transaction_id,
    }

    r = requests.post(
        f"{settings.OCTO_BASE_URL}/prepare_payment",
        json=payload,
        timeout=15,
    )
    r.raise_for_status()

    body = r.json()

    if body.get("error") != 0:
        raise OctoError(
            body.get("errMessage", "OCTO status tekshirishda xato")
        )

    return body["data"]

def verify_callback_signature(unique_key, octo_uuid, status, signature):
    raw = f"{unique_key}{octo_uuid}{status}"
    expected = hashlib.sha1(raw.encode()).hexdigest().upper()
    return hmac.compare_digest(expected, str(signature).upper())

def verify_callback_hash_key(
    unique_key: str,
    octo_uuid: str,
    status: str,
    hash_key: str,
) -> bool:
    raw = f"{unique_key}{octo_uuid}{status}"
    expected = hashlib.sha1(raw.encode()).hexdigest().upper()

    return hmac.compare_digest(
        expected,
        str(hash_key).upper(),
    )