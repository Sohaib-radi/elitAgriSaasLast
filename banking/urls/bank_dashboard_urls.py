from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.bank_dashboard_view import BankDashboardViewSet

router = DefaultRouter()
router.register(r"bank-dashboard", BankDashboardViewSet, basename="bank-dashboard")

urlpatterns = [
    path("", include(router.urls)),
]
