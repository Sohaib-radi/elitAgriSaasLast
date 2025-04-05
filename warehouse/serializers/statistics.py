from rest_framework import serializers
from warehouse.models.warehouse import Warehouse

class WarehouseStatisticsSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    warehouse_name = serializers.CharField()
    total_space = serializers.DecimalField(max_digits=10, decimal_places=2)
    used_space = serializers.DecimalField(max_digits=10, decimal_places=2)
    remaining_space = serializers.DecimalField(max_digits=10, decimal_places=2)
    usage_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

    def to_representation(self, instance):
        # instance is expected to be a Warehouse object
        total_space = instance.space
        used_space = sum(entry.space_taken for entry in instance.entries.all())

        return {
            "warehouse_id": instance.id,
            "warehouse_name": instance.name,
            "total_space": total_space,
            "used_space": used_space,
            "remaining_space": total_space - used_space,
            "usage_percentage": round((used_space / total_space) * 100 if total_space else 0, 2),
        }