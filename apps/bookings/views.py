from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView


from apps.payments import octo
from apps.payments.models import Payment
from .models import Booking, Extra, Location
from .serializers import (
    BookingCreateSerializer, BookingStatusSerializer, ExtraSerializer,
    LocationSerializer, QuoteSerializer,
)
from .services import build_quote, create_booking


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = None


class ExtraListView(ListAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    pagination_class = None

@extend_schema(
    request=QuoteSerializer,
    responses=QuoteSerializer,
)
class QuoteView(APIView):
    """Bron formasida narxni real vaqtda ko'rsatish uchun."""

    def post(self, request):
        s = QuoteSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        q = build_quote(car=d["car"], start_at=d["start_at"], end_at=d["end_at"],
                        pickup=d["pickup_location"], ret=d["return_location"], extras=d["extras"])
        q.pop("_items")
        return Response(q)

@extend_schema(
    request=BookingCreateSerializer,
)
class BookingCreateView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "booking"

    def post(self, request):
        s = BookingCreateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        booking = create_booking(
            car=d["car"], start_at=d["start_at"], end_at=d["end_at"],
            pickup=d["pickup_location"], ret=d["return_location"],
            customer_name=d["customer_name"], phone=d["phone"], email=d["email"],
            extras=d["extras"],
        )
        try:
            data = octo.prepare_payment(booking)
        except Exception:
            booking.status = Booking.Status.CANCELLED
            booking.save(update_fields=["status"])
            return Response({"detail": "To'lovni boshlab bo'lmadi. Keyinroq urinib ko'ring."},
                            status=status.HTTP_502_BAD_GATEWAY)

        Payment.objects.create(booking=booking, octo_uuid=data["octo_payment_UUID"], amount=booking.total_sum)
        return Response({"booking_id": booking.id, "pay_url": data["octo_pay_url"]},
                        status=status.HTTP_201_CREATED)


class BookingStatusView(RetrieveAPIView):
    queryset = Booking.objects.select_related("car")
    serializer_class = BookingStatusSerializer