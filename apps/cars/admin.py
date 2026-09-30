from django.contrib import admin

from .models import Car, CarImage, CarPrice, Category


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


class CarPriceInline(admin.TabularInline):
    model = CarPrice
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "klass", "seats", "deposit", "is_active")
    list_filter = ("category", "klass", "is_active")
    search_fields = ("name",)
    inlines = [CarPriceInline, CarImageInline]


admin.site.register(Category)