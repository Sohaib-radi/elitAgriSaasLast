from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from animal.models.field import CustomListField
from animal.serializers.field import CustomListFieldSerializer
from animal.filters.field import CustomListFieldFilter
from core.viewsets.base import AutoPermissionViewSet


class CustomFieldViewSet(AutoPermissionViewSet):
    """
    Read-only view for listing custom fields linked to an Animal List
    """
    serializer_class = CustomListFieldSerializer
    permission_module = "custom_fields"

    def get_queryset(self):
        return CustomListField.objects.filter(list_id=self.kwargs["list_id"])


class CustomListFieldViewSet(AutoPermissionViewSet):
    """
     Full CRUD for managing custom fields
    """
    serializer_class = CustomListFieldSerializer
    permission_module = "custom_fields"
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomListFieldFilter

    def get_queryset(self):
        return CustomListField.objects.filter(list__farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
