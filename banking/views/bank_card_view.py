from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.bank_card import BankCard
from banking.serializers.bank_card_serializer import BankCardSerializer

class BankCardViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing bank cards in a clean, scalable structure.
    """

    queryset = BankCard.objects.all().select_related("bank").order_by("-issue_date")
    serializer_class = BankCardSerializer
    permission_module = "banking"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["bank", "card_type", "status", "issue_date"]
    ordering_fields = ["issue_date", "expiry_date", "created_at"]
    search_fields = ["card_number", "holder_name", "note"]

    def perform_create(self, serializer):
        serializer.save()
