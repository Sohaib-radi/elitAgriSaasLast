from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db import transaction
from rest_framework.generics import RetrieveAPIView

from banking.serializers.loan_detailled_serializer import LoanDetailSerializer
from core.permissions.mixins import AutoPermissionMixin
from core.viewsets.base import AutoPermissionViewSet
from banking.models.loan import Loan
from banking.serializers.loan_serializer import LoanSerializer
from banking.utils.loan import generate_loan_payment_schedule

class LoanViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing loans in a professional, scalable, and clean manner.
    """

    queryset = Loan.objects.all().select_related("bank").order_by("-start_date")
    serializer_class = LoanSerializer
    permission_module = "loans"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["bank", "status", "repayment_method"]
    ordering_fields = ["start_date", "end_date", "amount", "created_at"]
    search_fields = ["loan_name", "loan_number", "description"]

    def perform_create(self, serializer):
        """
        Create loan and generate payment schedule atomically.
        If schedule generation fails, the loan will not be saved.
        """
        with transaction.atomic():
            loan = serializer.save(
                created_by=self.request.user,
                farm=self.request.user.active_farm
            )
            generate_loan_payment_schedule(loan,user=self.request.user)

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



class LoanDetailView(AutoPermissionMixin, RetrieveAPIView):
    permission_module = "loans"
    serializer_class = LoanDetailSerializer

    def get_queryset(self):
        return Loan.objects.select_related("bank").prefetch_related("payments").filter(
            farm=self.request.user.active_farm
        )