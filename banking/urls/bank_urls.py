from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.bank_view import BankViewSet

router = DefaultRouter()
router.register(r"banks", BankViewSet, basename="bank")

urlpatterns = [
    path("", include(router.urls)),
]