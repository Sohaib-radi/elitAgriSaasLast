from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.loan import Loan
from banking.serializers.loan_serializer import LoanSerializer

class LoanViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing loans in a professional, scalable, and clean manner.
    """

    queryset = Loan.objects.all().select_related("bank", "main_currency").order_by("-start_date")
    serializer_class = LoanSerializer
    permission_module = "banking"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["bank", "status", "repayment_method"]
    ordering_fields = ["start_date", "end_date", "amount", "created_at"]
    search_fields = ["loan_name", "loan_number", "description"]

    def perform_create(self, serializer):
        """
        Automatically link created_by for accountability.
        """
       
        serializer.save(
            created_by=self.request.user,
            farm=self.request.user.active_farm
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """
        Deactivate a loan (set status to closed) cleanly.
        """
        loan = self.get_object()
        loan.status = Loan.Status.CLOSED
        loan.save()
        return Response({"status": "Loan deactivated (closed)."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """
        Activate a loan (set status to active) cleanly.
        """
        loan = self.get_object()
        loan.status = Loan.Status.ACTIVE
        loan.save()
        return Response({"status": "Loan activated."}, status=status.HTTP_200_OK)
