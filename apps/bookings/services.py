import math
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.cars.models import Car
from .models import Booking, BookingExtra, Extra


def calc_days(start_at, end_at) -> int:
    """Har boshlangan 24 soat = 1 kun (kamida 1)."""
    return max(1, math.ceil((end_at - start_at).total_seconds() / 86400))


def daily_price(car: Car, days: int) -> int:
    prices = list(car.prices.all())
    if not prices:
        raise ValidationError({"car": "Bu avtomobil uchun tarif kiritilmagan."})
    for tier in prices:
        if tier.from_day <= days <= tier.to_day:
            return tier.price
    return prices[-1].price


def busy_bookings(start_at, end_at):
    """To'langan bronlar + 15 daqiqa ichidagi kutilayotganlar mashinani band qiladi."""
    hold_from = timezone.now() - timedelta(minutes=settings.BOOKING_HOLD_MINUTES)
    return Booking.objects.filter(start_at__lt=end_at, end_at__gt=start_at).filter(
        Q(status=Booking.Status.PAID)
        | Q(status=Booking.Status.PENDING, created_at__gte=hold_from)
    )


def is_available(car, start_at, end_at) -> bool:
    return not busy_bookings(start_at, end_at).filter(car=car).exists()


def build_quote(*, car, start_at, end_at, pickup, ret, extras) -> dict:
    """Narx FAQAT serverda hisoblanadi; frontend summa yubormaydi."""
    days = calc_days(start_at, end_at)
    per_day = daily_price(car, days)
    rent = per_day * days

    qty_by_code: dict = {}
    for e in extras:
        qty_by_code[e["code"]] = qty_by_code.get(e["code"], 0) + e["qty"]
    extra_objs = list(Extra.objects.filter(code__in=qty_by_code))
    if len(extra_objs) != len(qty_by_code):
        raise ValidationError({"extras": "Noma'lum qo'shimcha xizmat."})
    items = [(x, qty_by_code[x.code]) for x in extra_objs]

    extras_sum = sum(x.price * q for x, q in items)
    fees = pickup.fee + ret.fee
    return {
        "days": days, "daily_price": per_day, "rent_sum": rent,
        "extras_sum": extras_sum, "fees_sum": fees,
        "total_sum": rent + extras_sum + fees,
        "km_limit": car.daily_limit_km * days, "deposit": car.deposit,
        "_items": items,
    }


@transaction.atomic
def create_booking(*, car, start_at, end_at, pickup, ret, customer_name, phone, email, extras) -> Booking:
    Car.objects.select_for_update().get(pk=car.pk)  # bir vaqtda ikki bronning oldini oladi
    if not is_available(car, start_at, end_at):
        raise ValidationError({"car": "Bu sanalarda avtomobil band."})

    q = build_quote(car=car, start_at=start_at, end_at=end_at, pickup=pickup, ret=ret, extras=extras)
    booking = Booking.objects.create(
        car=car, start_at=start_at, end_at=end_at, pickup_location=pickup, return_location=ret,
        customer_name=customer_name, phone=phone, email=email, days=q["days"],
        rent_sum=q["rent_sum"], extras_sum=q["extras_sum"], fees_sum=q["fees_sum"],
        total_sum=q["total_sum"],
    )
    BookingExtra.objects.bulk_create([
        BookingExtra(booking=booking, extra=x, qty=qty, unit_price=x.price) for x, qty in q["_items"]
    ])
    return booking