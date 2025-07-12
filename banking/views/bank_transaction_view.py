from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.bank_transaction import BankTransaction
from banking.serializers.bank_transaction_serializer import BankTransactionSerializer

class BankTransactionViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing bank transactions in a scalable, clean structure.
    """

    queryset = BankTransaction.objects.all().select_related("bank", "loan").order_by("-transaction_date")
    serializer_class = BankTransactionSerializer
    permission_module = "banking"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["bank", "transaction_type", "payment_method", "loan", "status", "transaction_date"]
    ordering_fields = ["transaction_date", "amount", "created_at"]
    search_fields = ["reference", "note"]

    def perform_create(self, serializer):
        serializer.save()
