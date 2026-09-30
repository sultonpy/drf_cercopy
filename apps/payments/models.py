from django.db import models

from apps.bookings.models import Booking


class Payment(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Yaratildi"
        SUCCEEDED = "succeeded", "Muvaffaqiyatli"
        CANCELED = "canceled", "Bekor qilindi"

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    octo_uuid = models.CharField(max_length=64, unique=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CREATED)
    raw_notify = models.JSONField(null=True, blank=True)  # audit uchun webhook nusxasi
    created_at = models.DateTimeField(auto_now_add=True)


class MockOctoTransaction(models.Model):
    """FAQAT mock rejim: soxta Octo serverining holati."""
    uuid = models.CharField(max_length=64, unique=True)
    shop_transaction_id = models.CharField(max_length=64)
    total_sum = models.PositiveIntegerField()
    notify_url = models.URLField(max_length=500)
    return_url = models.URLField(max_length=500)