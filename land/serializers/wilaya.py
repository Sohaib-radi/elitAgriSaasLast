from rest_framework import serializers
from land.models.wilaya import Wilaya


class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = [
            "id", "name", "code", "created_at", "created_by"
        ]
        read_only_fields = ["id", "created_at", "created_by"]
