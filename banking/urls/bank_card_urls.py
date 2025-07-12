from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.bank_card_view import BankCardViewSet

router = DefaultRouter()
router.register(r"bank-cards", BankCardViewSet, basename="bank-card")

urlpatterns = [
    path("", include(router.urls)),
]
