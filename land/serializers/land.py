from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from land.models.land import Land
from core.serializers.user import UserSimpleSerializer  

class LandSerializer(serializers.ModelSerializer):
    current_owner = UserSimpleSerializer(read_only=True)
    previous_owner = UserSimpleSerializer(read_only=True)
    wilaya_name = serializers.CharField(source="wilaya.name", read_only=True)

    class Meta:
        model = Land
        fields = [
            "id",
            "code",
            "international_number",
            "land_number",
            "wilaya",
            "wilaya_name",
            "address",
            "latitude",
            "longitude",
            "google_maps_url",
            "price",
            "purchase_date",
            "land_type",
            "status",
            "area",
            "description",
            "current_owner",
            "previous_owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "code", "created_at", "updated_at", "current_owner", "previous_owner", "wilaya_name"
        ]
