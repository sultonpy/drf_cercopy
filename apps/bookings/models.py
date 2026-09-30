import uuid

from django.db import models

from apps.cars.models import Car


class Location(models.Model):
    name = models.CharField(max_length=120)
    fee = models.PositiveIntegerField(default=0, help_text="Shu joyda topshirish/olish uchun to'lov")

    def __str__(self):
        return self.name


class Extra(models.Model):
    code = models.SlugField(unique=True)  # wifi, insurance, child_seat, fridge, driver
    name = models.CharField(max_length=80)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        PAID = "paid", "To'landi"
        CANCELLED = "cancelled", "Bekor qilindi"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # = shop_transaction_id
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="bookings")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    pickup_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="+")
    return_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="+")
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    days = models.PositiveSmallIntegerField()
    rent_sum = models.PositiveIntegerField()
    extras_sum = models.PositiveIntegerField(default=0)
    fees_sum = models.PositiveIntegerField(default=0)
    total_sum = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.car} | {self.customer_name} | {self.status}"


class BookingExtra(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="items")
    extra = models.ForeignKey(Extra, on_delete=models.PROTECT)
    qty = models.PositiveSmallIntegerField(default=1)
    unit_price = models.PositiveIntegerField()  # bron paytidagi narx