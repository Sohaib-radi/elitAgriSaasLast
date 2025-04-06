from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from warehouse.models.warehouse import Warehouse
from warehouse.models.entry import WarehouseEntry
from warehouse.serializers.statistics import WarehouseStatisticsSerializer
from core.permissions.permissions import HasRolePermission
from core.viewsets.base import AutoPermissionAPIView
class WarehouseStatisticsView(AutoPermissionAPIView):
    permission_module = "warehouse"
    
    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse, id=pk, farm=request.user.active_farm)

        entries = WarehouseEntry.objects.filter(warehouse=warehouse)

        total_quantity = sum(entry.quantity for entry in entries)
        total_weight = sum(entry.weight for entry in entries)
        total_space_used = sum(entry.space_taken for entry in entries)
        used_percentage = round((total_space_used / warehouse.space) * 100, 2) if warehouse.space else 0

        type_counts = {}
        for entry in entries:
            model_name = entry.content_type.model
            type_counts[model_name] = type_counts.get(model_name, 0) + 1

        latest_entries = entries.order_by("-date_added")[:5]

        data = {
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "total_entries": entries.count(),
            "total_quantity": total_quantity,
            "total_weight": total_weight,
            "total_space_used": total_space_used,
            "space_available": warehouse.space - total_space_used,
            "used_percentage": used_percentage,
            "entries_by_type": type_counts,
            "latest_entries": [
                {
                    "object": str(e.content_object),
                    "date_added": e.date_added,
                    "quantity": e.quantity,
                    "weight": e.weight,
                    "space_taken": e.space_taken,
                }
                for e in latest_entries
            ],
        }

        return Response(data)
