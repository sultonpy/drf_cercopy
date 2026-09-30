from django.db import models


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Car(models.Model):
    class Klass(models.TextChoices):
        ECONOMY = "economy", "Ekonom"
        MIDDLE = "middle", "O'rta"
        PREMIUM = "premium", "Premium"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="cars")
    klass = models.CharField(max_length=10, choices=Klass.choices)
    seats = models.PositiveSmallIntegerField()
    doors = models.PositiveSmallIntegerField(default=4)
    fuel_per_100 = models.DecimalField(max_digits=4, decimal_places=1)
    min_experience = models.PositiveSmallIntegerField(default=4)
    daily_limit_km = models.PositiveIntegerField(default=300)
    deposit = models.PositiveIntegerField()
    features = models.JSONField(default=list, blank=True)  # ["ac","auto","abs","airbag","parking_sensor"]
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="cars/")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


class CarPrice(models.Model):
    """Muddatga qarab tarif: from_day..to_day kun uchun BIR KUNLIK narx."""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="prices")
    from_day = models.PositiveSmallIntegerField()
    to_day = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ["from_day"]