

from rest_framework import viewsets, status
from rest_framework.response import Response
from warehouse.models import Warehouse, WarehouseImage, WarehouseVideo
from warehouse.serializers.warehouse import (
    WarehouseSerializer,
    WarehouseImageSerializer,
    WarehouseVideoSerializer,
)
from core.viewsets.base import AutoPermissionViewSet


class WarehouseViewSet(AutoPermissionViewSet):
    """
    ViewSet to manage Warehouses for a farm.
    """
    serializer_class = WarehouseSerializer
    permission_module = "warehouses"

    def get_queryset(self):
        return Warehouse.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )


class WarehouseImageViewSet(AutoPermissionViewSet):
    """
    Manage warehouse image gallery
    """
    serializer_class = WarehouseImageSerializer
    permission_module = "warehouses"

    def get_queryset(self):
        return WarehouseImage.objects.filter(warehouse__farm=self.request.user.active_farm)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": "Failed to upload image.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WarehouseVideoViewSet(AutoPermissionViewSet):
    """
    Manage warehouse video gallery
    """
    serializer_class = WarehouseVideoSerializer
    permission_module = "warehouses"

    def get_queryset(self):
        return WarehouseVideo.objects.filter(warehouse__farm=self.request.user.active_farm)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": "Failed to upload video.", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
