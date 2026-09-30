from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from apps.auth_views import MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.bookings.views import (
    BookingCreateView, BookingStatusView, ExtraListView, LocationListView, QuoteView,
)
from apps.cars.views import CarViewSet, CategoryViewSet
from apps.content.views import FAQListView, PostViewSet, ReviewListView
from apps.payments.views import OctoNotifyView

router = DefaultRouter()
router.register("cars", CarViewSet, basename="car")
router.register("categories", CategoryViewSet, basename="category")
router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/me/", MeView.as_view(), name="auth_me"),
    path("api/locations/", LocationListView.as_view()),
    path("api/extras/", ExtraListView.as_view()),
    path("api/faq/", FAQListView.as_view()),
    path("api/reviews/", ReviewListView.as_view()),
    path("api/bookings/quote/", QuoteView.as_view()),
    path("api/bookings/", BookingCreateView.as_view()),
    path("api/bookings/<uuid:pk>/", BookingStatusView.as_view()),
    path("api/payments/octo/notify/", OctoNotifyView.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]


if settings.PAYMENT_MODE == "mock":
    from apps.payments import mock_octo
    urlpatterns += [
        path("mock-octo/prepare_payment", mock_octo.prepare_payment),
        path("mock-octo/pay/<str:uuid>/", mock_octo.pay_page),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)