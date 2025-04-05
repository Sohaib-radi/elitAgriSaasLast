from rest_framework import serializers
from crop.models.land_status import LandStatus, LandStatusChoices

class LandStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = LandStatus
        fields = [
            "id",
            "agricultural_land",
            "status",
            "status_display",
            "description",
            "product_used",
            "quantity_used",
            "date",
        ]
        read_only_fields = ["id", "status_display"]
