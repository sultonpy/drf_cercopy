from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from apps.bookings.services import busy_bookings
from .models import Car, Category
from .serializers import CarDetailSerializer, CarListSerializer, CategorySerializer


def _parse_dt(value, name):
    dt = parse_datetime(value) if value else None
    if dt is None:
        raise ValidationError({name: "Noto'g'ri sana formati (ISO 8601 kutilmoqda)."})
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None

    def get_serializer_class(self):
        return CarDetailSerializer if self.action == "retrieve" else CarListSerializer

    def get_queryset(self):
        qs = (Car.objects.filter(is_active=True)
              .select_related("category").prefetch_related("prices", "images"))
        p = self.request.query_params
        if p.get("category"):
            qs = qs.filter(category__slug=p["category"])
        if p.get("start") or p.get("end"):  # faqat bo'sh mashinalar
            start, end = _parse_dt(p.get("start"), "start"), _parse_dt(p.get("end"), "end")
            if end <= start:
                raise ValidationError({"end": "end start'dan keyin bo'lishi kerak."})
            qs = qs.exclude(id__in=busy_bookings(start, end).values("car_id"))
        return qs