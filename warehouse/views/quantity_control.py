from rest_framework import viewsets
from warehouse.models.quantity_control import WarehouseQuantitySchedule, WarehouseReminder
from warehouse.serializers.quantity_control import WarehouseQuantityScheduleSerializer, WarehouseReminderSerializer
from core.viewsets.base import AutoPermissionViewSet

class WarehouseQuantityScheduleViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    Manage quantity automation (increase/decrease) for warehouse items.
    """
    serializer_class = WarehouseQuantityScheduleSerializer
    permission_module = "warehouses"

    def get_queryset(self):
        return WarehouseQuantitySchedule.objects.filter(
            warehouse__farm=self.request.user.active_farm
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class WarehouseReminderViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    Manage reminders for low quantity alerts.
    """
    serializer_class = WarehouseReminderSerializer
    permission_module = "warehouses"

    def get_queryset(self):
        return WarehouseReminder.objects.filter(
            warehouse__farm=self.request.user.active_farm
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
