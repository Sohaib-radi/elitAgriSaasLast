from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.bank_transaction_view import BankTransactionViewSet

router = DefaultRouter()
router.register(r"bank-transactions", BankTransactionViewSet, basename="bank-transaction")

urlpatterns = [
    path("", include(router.urls)),
]
