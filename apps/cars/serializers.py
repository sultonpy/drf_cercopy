from rest_framework import serializers

from root.utils import pick_lang
from .models import Car, CarImage, CarPrice, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "name"]


class CarPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPrice
        fields = ["from_day", "to_day", "price"]


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ["image"]


class CarListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    cover = serializers.SerializerMethodField()
    price_from = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ["id", "name", "category", "klass", "seats", "daily_limit_km",
                  "deposit", "features", "cover", "price_from"]

    def get_cover(self, obj):
        img = next(iter(obj.images.all()), None)
        if not img:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(img.image.url) if request else img.image.url

    def get_price_from(self, obj):
        prices = list(obj.prices.all())
        return prices[0].price if prices else None


class CarDetailSerializer(CarListSerializer):
    prices = CarPriceSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    description = serializers.SerializerMethodField()

    class Meta(CarListSerializer.Meta):
        fields = CarListSerializer.Meta.fields + [
            "doors", "fuel_per_100", "min_experience", "prices", "images", "description",
        ]

    def get_description(self, obj):
        return pick_lang(obj, "description", self.context.get("request"))