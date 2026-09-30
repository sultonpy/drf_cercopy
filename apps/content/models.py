from django.db import models
from django.utils import timezone


class Post(models.Model):
    slug = models.SlugField(unique=True)
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200, blank=True)
    body_uz = models.TextField()
    body_ru = models.TextField(blank=True)
    cover = models.ImageField(upload_to="posts/", blank=True, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title_uz


class FAQ(models.Model):
    question_uz = models.CharField(max_length=250)
    question_ru = models.CharField(max_length=250, blank=True)
    answer_uz = models.TextField()
    answer_ru = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

    def __str__(self):
        return self.question_uz


class Review(models.Model):
    author = models.CharField(max_length=80)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)  # moderatsiyadan keyin

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} ({self.rating}/5)"