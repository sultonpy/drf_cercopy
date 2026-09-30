from django.contrib import admin

from .models import FAQ, Post, Review

admin.site.register(Post)
admin.site.register(FAQ)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "rating", "is_published", "created_at")
    list_filter = ("is_published",)