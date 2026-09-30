from django.utils import timezone
from rest_framework import serializers

from apps.cars.models import Car
from .models import Booking, Extra, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name", "fee"]


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ["code", "name", "price"]


class ExtraQtySerializer(serializers.Serializer):
    code = serializers.SlugField()
    qty = serializers.IntegerField(min_value=1, max_value=10, default=1)


class QuoteSerializer(serializers.Serializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.filter(is_active=True))
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    pickup_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    return_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    extras = ExtraQtySerializer(many=True, required=False, default=list)

    def validate(self, attrs):
        if attrs["end_at"] <= attrs["start_at"]:
            raise serializers.ValidationError("Qaytarish sanasi olish sanasidan keyin bo'lishi kerak.")
        if attrs["start_at"] < timezone.now():
            raise serializers.ValidationError("O'tgan sanaga bron qilib bo'lmaydi.")
        return attrs


class BookingCreateSerializer(QuoteSerializer):
    customer_name = serializers.CharField(min_length=2, max_length=100)
    phone = serializers.RegexField(r"^\+?\d{9,15}$", error_messages={"invalid": "Telefon raqami noto'g'ri."})
    email = serializers.EmailField(required=False, allow_blank=True, default="")


class BookingStatusSerializer(serializers.ModelSerializer):
    car_name = serializers.CharField(source="car.name")

    class Meta:
        model = Booking
        fields = ["id", "status", "car_name", "start_at", "end_at", "days", "total_sum"]