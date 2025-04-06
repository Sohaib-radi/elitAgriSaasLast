

from rest_framework import serializers
from warehouse.models import Warehouse, WarehouseImage, WarehouseVideo

class WarehouseSerializer(serializers.ModelSerializer):
    google_maps_url = serializers.ReadOnlyField()

    class Meta:
        model = Warehouse
        fields = [
            "id", "name", "description", "space", "latitude", "longitude",
            "image", "google_maps_url", "created_by", "created_at"
        ]
        read_only_fields = ["id", "created_by", "created_at", "google_maps_url"]

class WarehouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseImage
        fields = [
            "id", "warehouse", "image", "title", "description", "uploaded_at"
        ]
        read_only_fields = ["id", "uploaded_at"]

class WarehouseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseVideo
        fields = [
            "id", "warehouse", "video", "title", "description", "uploaded_at"
        ]
        read_only_fields = ["id", "uploaded_at"]
