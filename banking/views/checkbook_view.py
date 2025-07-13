from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.viewsets.base import AutoPermissionViewSet
from banking.models.checkbook import Checkbook
from banking.serializers.checkbook_serializer import CheckbookSerializer

class CheckbookViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    API endpoint for managing checkbooks in a clean, scalable structure.
    """

    queryset = Checkbook.objects.all().select_related("bank").order_by("-issue_date")
    serializer_class = CheckbookSerializer
    permission_module = "checkbooks"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["bank", "status", "issue_date"]
    ordering_fields = ["issue_date", "created_at"]
    search_fields = ["note"]

    def perform_create(self, serializer):
        serializer.save()
