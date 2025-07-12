from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.models.attachment import Attachment
from core.serializers.attachment_serializer import AttachmentSerializer
from core.viewsets.base import AutoPermissionViewSet

class AttachmentViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    Professional, reusable API endpoint for managing attachments globally.
    """

    queryset = Attachment.objects.all().select_related("content_type", "uploaded_by").order_by("-created_at")
    serializer_class = AttachmentSerializer
    permission_module = "core"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["content_type", "object_id", "file_type", "uploaded_by", "is_public", "created_at"]
    ordering_fields = ["created_at", "name", "size"]
    search_fields = ["name", "description", "file"]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
