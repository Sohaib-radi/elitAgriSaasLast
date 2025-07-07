from rest_framework import serializers
from warehouse.models.warehouse import Warehouse
from decimal import Decimal, ROUND_HALF_UP

class WarehouseStatisticsSerializer(serializers.Serializer):
    """
    Serializer to compute warehouse space usage statistics.
    """
    warehouse_id = serializers.IntegerField()
    warehouse_name = serializers.CharField()
    total_space = serializers.DecimalField(max_digits=10, decimal_places=2)
    used_space = serializers.DecimalField(max_digits=10, decimal_places=2)
    remaining_space = serializers.DecimalField(max_digits=10, decimal_places=2)
    usage_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

    def to_representation(self, instance: Warehouse):
        total_space = instance.space
        used_space = sum(entry.space_taken or Decimal('0.00') for entry in instance.entries.all())
        remaining_space = total_space - used_space

        usage_percentage = (
            (used_space / total_space * Decimal('100'))
            .quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            if total_space else Decimal('0.00')
        )

        return {
            "warehouse_id": instance.id,
            "warehouse_name": instance.name,
            "total_space": total_space,
            "used_space": used_space,
            "remaining_space": remaining_space,
            "usage_percentage": usage_percentage,
        }
