import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")

import django
django.setup()

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from apps.bookings.models import Extra, Location
from apps.cars.models import Car, CarPrice, Category



@pytest.fixture(autouse=True)
def _clear_cache():
    cache.clear()  # throttle hisoblagichini tozalaydi


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def setup_data(db):
    cat = Category.objects.create(slug="sedan", name="Sedan")
    car = Car.objects.create(name="Test Car", category=cat, klass="economy", seats=5,
                             fuel_per_100=7, deposit=3_000_000)
    CarPrice.objects.create(car=car, from_day=1, to_day=3, price=100_000)
    CarPrice.objects.create(car=car, from_day=4, to_day=7, price=90_000)
    city = Location.objects.create(name="Markaz", fee=0)
    airport = Location.objects.create(name="Aeroport", fee=200_000)
    Extra.objects.create(code="wifi", name="Wi-Fi", price=100_000)
    return {"car": car, "city": city, "airport": airport}