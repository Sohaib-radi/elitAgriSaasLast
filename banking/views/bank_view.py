from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.bank import Bank
from banking.serializers.bank_serializer import BankSerializer

class BankViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing banks in a clean, scalable, and professional way.
    """

    queryset = Bank.objects.all().select_related("main_currency").order_by("name")
    serializer_class = BankSerializer
    permission_module = "banks"

    # Add filtering, ordering, searching
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["main_currency", "bank_number"]
    ordering_fields = ["name", "account_number", "created_at"]
    search_fields = ["name", "account_number", "bank_number", "email", "phone_number"]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            farm=self.request.user.active_farm
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """
        Custom action to deactivate a bank cleanly.
        """
        bank = self.get_object()
        bank.is_active = False
        bank.save()
        return Response({"status": "Bank deactivated."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """
        Custom action to activate a bank cleanly.
        """
        bank = self.get_object()
        bank.is_active = True
        bank.save()
        return Response({"status": "Bank activated."}, status=status.HTTP_200_OK)
