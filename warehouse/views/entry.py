from rest_framework import viewsets, status
from rest_framework.response import Response
from warehouse.models.entry import WarehouseEntry
from warehouse.serializers.entry import WarehouseEntrySerializer
from core.viewsets.base import AutoPermissionViewSet
from rest_framework.permissions import IsAuthenticated

class WarehouseEntryViewSet( viewsets.ModelViewSet):
    """
    Manage entries in a warehouse (products, crops, animals, etc.)
    Uses generic foreign key for flexibility.
    """

    serializer_class = WarehouseEntrySerializer
    #permission_module = "warehouse"

    # 🚩 Temporarily override central permissions to avoid permission issues
    permission_classes = [IsAuthenticated]  # allow any authenticated user for now

    def get_queryset(self):
        return WarehouseEntry.objects.filter(
            warehouse__farm=self.request.user.active_farm
        ).select_related("warehouse", "content_type").order_by("-date_added")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

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