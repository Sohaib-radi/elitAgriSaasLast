from rest_framework import serializers
from crop.models.crop import Crop, CropStatusChoices, UsageChoices, UnitChoices

class CropSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    usage_display = serializers.CharField(source="get_usage_display", read_only=True)
    unit_display = serializers.CharField(source="get_unit_display", read_only=True)

    class Meta:
        model = Crop
        fields = [
            "id",
            "agricultural_land",
            "crop_type",
            "status",
            "status_display",
            "quantity",
            "unit",
            "unit_display",
            "usage",
            "usage_display",
            "description",
            "date",
        ]
        read_only_fields = ["id", "status_display", "usage_display", "unit_display"]
