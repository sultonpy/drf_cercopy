from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.bookings.models import Extra, Location
from apps.cars.models import Car, CarPrice, Category
from apps.content.models import FAQ, Post, Review

CATEGORIES = [("budget", "Byudjetlilar"), ("sedan", "Sedan"), ("crossover", "Krossoverlar"),
              ("suv", "Yo'l tanlamaslar"), ("minivan", "Minivenlar"), ("pickup", "Pikaplar")]

ALL = ["ac", "auto", "parking_sensor", "airbag", "abs"]
# (nomi, kategoriya, klass, o'rindiq, eshik, yoqilg'i, kunlik narx, depozit, xususiyatlar, tavsif)
CARS = [
    ("Chevrolet Spark", "budget", "economy", 4, 5, 6.0, 280_000, 3_000_000, ALL, "Shahar uchun ixcham va tejamkor avtomobil."),
    ("Chevrolet Cobalt", "budget", "economy", 5, 4, 7.0, 380_000, 3_000_000, ["ac", "airbag", "abs"], "Kundalik yurish uchun qulay sedan."),
    ("Chevrolet Lacetti", "sedan", "economy", 5, 4, 8.0, 430_000, 3_000_000, ["ac", "airbag", "abs"], "Keng salonli klassik sedan."),
    ("Kia K5", "sedan", "middle", 5, 4, 8.5, 1_100_000, 4_000_000, ALL, "Zamonaviy biznes-klass sedan."),
    ("Chevrolet Tracker", "crossover", "middle", 5, 5, 7.5, 680_000, 4_000_000, ALL, "Shahar va sayohat uchun krossover."),
    ("Kia Sonet", "crossover", "middle", 5, 5, 7.0, 680_000, 4_000_000, ["ac", "auto", "airbag", "abs"], "Baland o'tirish va tejamkorlik."),
    ("Toyota Land Cruiser Prado", "suv", "middle", 7, 5, 12.0, 1_050_000, 4_000_000, ALL, "7 o'rindiqli kuchli yo'l tanlamas."),
    ("Kia Carnival", "minivan", "middle", 7, 5, 10.0, 1_050_000, 4_000_000, ALL, "Katta oila va guruhlar uchun minivan."),
    ("Isuzu D-Max", "pickup", "middle", 4, 4, 9.5, 1_400_000, 4_000_000, ["ac", "auto", "airbag", "abs"], "Yuk va og'ir yo'llar uchun pikap."),
    ("Toyota Land Cruiser 300", "suv", "premium", 7, 5, 13.0, 2_900_000, 5_000_000, ALL, "Premium yo'l tanlamas."),
]
TIERS = [(1, 3, 1.00), (4, 7, 0.95), (8, 14, 0.92), (15, 30, 0.83)]
EXTRAS = [("wifi", "Wi-Fi router", 100_000), ("insurance", "Qo'shimcha sug'urta", 50_000),
          ("child_seat", "Bola o'rindig'i", 100_000), ("fridge", "Muzlatgich", 200_000),
          ("driver", "Qo'shimcha haydovchi", 100_000)]
FAQS = [
    ("Qanday hujjatlar kerak?", "Pasport va amaldagi haydovchilik guvohnomasi.",
     "Какие документы нужны?", "Паспорт и действующее водительское удостоверение."),
    ("Depozit qachon qaytariladi?", "Avtomobil qabul qilinib, jarima va shikastlar tekshirilgach.",
     "Когда возвращается залог?", "После приёмки автомобиля и проверки штрафов и повреждений."),
    ("Kunlik kilometr limiti qancha?", "Kuniga 300 km. Oshgan kilometrlar uchun qo'shimcha to'lov olinadi.",
     "Какой лимит пробега?", "300 км в сутки. За превышение взимается доплата."),
    ("Yoqilg'i siyosati qanday?", "To'liq bak bilan beriladi va to'liq bak bilan qaytariladi.",
     "Топливная политика?", "Выдаётся с полным баком и возвращается с полным баком."),
]


class Command(BaseCommand):
    help = "Demo ma'lumotlarni yuklaydi (qayta ishga tushirsa ham xavfsiz)."

    def handle(self, *args, **opts):
        cats = {s: Category.objects.update_or_create(slug=s, defaults={"name": n})[0] for s, n in CATEGORIES}
        for name, cat, klass, seats, doors, fuel, price, dep, feats, desc in CARS:
            car, created = Car.objects.update_or_create(name=name, defaults=dict(
                category=cats[cat], klass=klass, seats=seats, doors=doors, fuel_per_100=fuel,
                deposit=dep, features=feats, description_uz=desc, description_ru=desc))
            if created:
                CarPrice.objects.bulk_create([
                    CarPrice(car=car, from_day=a, to_day=b, price=round(price * k / 1000) * 1000)
                    for a, b, k in TIERS])
        Location.objects.get_or_create(name="Toshkent, shahar markazi", defaults={"fee": 0})
        Location.objects.get_or_create(name="Toshkent xalqaro aeroporti (TAS)", defaults={"fee": 200_000})
        for code, name, price in EXTRAS:
            Extra.objects.update_or_create(code=code, defaults={"name": name, "price": price})
        if not FAQ.objects.exists():
            for i, (qu, au, qr, ar) in enumerate(FAQS):
                FAQ.objects.create(question_uz=qu, answer_uz=au, question_ru=qr, answer_ru=ar, order=i)
        if not Post.objects.exists():
            now = timezone.now()
            Post.objects.create(slug="ijaraga-olishdan-oldin", title_uz="Avtomobil ijarasi: nimalarni bilish kerak",
                                title_ru="Аренда авто: что нужно знать", published_at=now - timedelta(days=10),
                                body_uz="Ijaraga olishdan oldin hujjatlar, depozit, kilometr limiti va yoqilg'i siyosatini aniqlang.",
                                body_ru="Перед арендой уточните документы, залог, лимит пробега и топливную политику.")
            Post.objects.create(slug="toshkent-marshruti", title_uz="Toshkentda 1–2 kunlik marshrut",
                                title_ru="Маршрут по Ташкенту на 1–2 дня", published_at=now - timedelta(days=3),
                                body_uz="Tarixiy joylar, muzeylar va bog'larni mashinada aylanib chiqish uchun marshrut.",
                                body_ru="Маршрут по историческим местам, музеям и паркам на автомобиле.")
        if not Review.objects.exists():  # DEMO; haqiqiylarini admin orqali kiriting
            Review.objects.create(author="Demo Mijoz", text="Mashina toza, hujjatlar tez rasmiylashtirildi.", rating=5, is_published=True)
            Review.objects.create(author="Demo Mijoz 2", text="Aeroportda o'z vaqtida topshirishdi.", rating=5, is_published=True)
        self.stdout.write(self.style.SUCCESS(f"Seed tayyor: {Car.objects.count()} ta avtomobil."))