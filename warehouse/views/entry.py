

from rest_framework import viewsets, status
from rest_framework.response import Response
from warehouse.models.entry import WarehouseEntry
from warehouse.serializers.entry import WarehouseEntrySerializer
from core.viewsets.base import AutoPermissionViewSet

class WarehouseEntryViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    Manage entries in a warehouse (products, crops, animals, etc.)
    Uses generic foreign key for flexibility.
    """
    serializer_class = WarehouseEntrySerializer
    permission_module = "warehouses"

    def get_queryset(self):
        return WarehouseEntry.objects.filter(
            warehouse__farm=self.request.user.active_farm
        ).select_related("warehouse", "content_type")

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
