from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from warehouse.models.warehouse import Warehouse
from warehouse.models.entry import WarehouseEntry
from core.viewsets.base import AutoPermissionAPIView
from decimal import Decimal, ROUND_HALF_UP

class WarehouseStatisticsView(AutoPermissionAPIView):
    """
    Retrieve detailed statistics for a specific warehouse,
    including quantities, space usage, breakdown by type, and recent entries.
    """
    permission_module = "warehouse"

    def get(self, request, pk):
        warehouse = get_object_or_404(Warehouse, id=pk, farm=request.user.active_farm)

        entries = WarehouseEntry.objects.filter(warehouse=warehouse).order_by("-date_added")

        total_quantity = sum(entry.quantity for entry in entries)
        total_weight = sum(entry.weight or 0 for entry in entries)
        total_space_used = sum(entry.space_taken or 0 for entry in entries)
        used_percentage = (
            (Decimal(total_space_used) / Decimal(warehouse.space) * Decimal(100))
            .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if warehouse.space else Decimal("0.00")
        )

        type_counts = {}
        for entry in entries:
            model_name = entry.content_type.model
            type_counts[model_name] = type_counts.get(model_name, 0) + 1

        latest_entries = entries[:5]

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
