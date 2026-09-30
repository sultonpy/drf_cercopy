from django.contrib import admin

from .models import Booking, BookingExtra, Extra, Location


class BookingExtraInline(admin.TabularInline):
    model = BookingExtra
    extra = 0
    readonly_fields = ("extra", "qty", "unit_price")
    can_delete = False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "customer_name", "phone", "start_at", "end_at", "total_sum", "status")
    list_filter = ("status", "car")
    search_fields = ("customer_name", "phone")
    readonly_fields = ("days", "rent_sum", "extras_sum", "fees_sum", "total_sum", "created_at")
    inlines = [BookingExtraInline]


admin.site.register(Location)
admin.site.register(Extra)