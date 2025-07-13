from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.check import Check
from banking.serializers.check_serializer import CheckSerializer

class CheckViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing checks in a clean, scalable structure.
    """

    queryset = Check.objects.all().select_related("checkbook", "transaction").order_by("-due_date")
    serializer_class = CheckSerializer
    permission_module = "checks"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["checkbook", "status", "payment_status", "direction", "due_date", "issue_date"]
    ordering_fields = ["due_date", "issue_date", "amount", "created_at"]
    search_fields = ["beneficiary_name", "check_number", "note"]

    def perform_create(self, serializer):
        serializer.save()
