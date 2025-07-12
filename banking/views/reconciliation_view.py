from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.reconciliation import Reconciliation
from banking.serializers.reconciliation_serializer import ReconciliationSerializer

class ReconciliationViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing reconciliations in a clean, scalable structure.
    """

    queryset = Reconciliation.objects.all().select_related(
        "bank_transaction", "loan_payment", "linked_check"
    ).order_by("-reconciliation_date")
    serializer_class = ReconciliationSerializer
    permission_module = "banking"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["bank_transaction", "loan_payment", "linked_check", "status", "reconciliation_date"]
    ordering_fields = ["reconciliation_date", "reconciled_amount", "created_at"]
    search_fields = ["note"]

    def perform_create(self, serializer):
        serializer.save()
