from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.loan_payment_view import LoanPaymentViewSet

router = DefaultRouter()
router.register(r"loan-payments", LoanPaymentViewSet, basename="loan-payment")

urlpatterns = [
    path("", include(router.urls)),
]
