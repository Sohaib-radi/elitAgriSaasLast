from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.loan_payment import LoanPayment
from banking.serializers.loan_payment_serializer import LoanPaymentSerializer

class LoanPaymentViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing loan payments cleanly and professionally.
    """

    queryset = LoanPayment.objects.all().select_related("loan").order_by("-payment_date")
    serializer_class = LoanPaymentSerializer
    permission_module = "loan_payments"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["loan", "status", "payment_method", "payment_date"]
    ordering_fields = ["payment_date", "amount_paid", "created_at"]
    search_fields = ["payment_reference", "note"]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            farm=self.request.user.active_farm
        )
