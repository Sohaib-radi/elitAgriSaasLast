from rest_framework import serializers
from warehouse.models import Warehouse, WarehouseImage, WarehouseVideo

class WarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer for Warehouse, exposing location, media, and metadata.
    """
    google_maps_url = serializers.ReadOnlyField()

    class Meta:
        model = Warehouse
        fields = [
            "id", "name", "description", "space", "is_active",
            "latitude", "longitude", "image", "google_maps_url",
            "created_by", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at", "google_maps_url"]

class WarehouseImageSerializer(serializers.ModelSerializer):
    """
    Serializer for images linked to a warehouse.
    """
    class Meta:
        model = WarehouseImage
        fields = [
            "id", "warehouse", "image", "title", "description", "uploaded_at"
        ]
        read_only_fields = ["id", "uploaded_at"]

class WarehouseVideoSerializer(serializers.ModelSerializer):
    """
    Serializer for videos linked to a warehouse.
    """
    class Meta:
        model = WarehouseVideo
        fields = [
            "id", "warehouse", "video", "title", "description", "uploaded_at"
        ]
        read_only_fields = ["id", "uploaded_at"]
