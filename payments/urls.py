from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, mock_gateway

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("payments/mock-gateway/", mock_gateway, name="mock-gateway"),
] + router.urls