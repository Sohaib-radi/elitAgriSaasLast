from rest_framework import serializers
from crop.models.agricultural_land import AgriculturalLand

class AgriculturalLandSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgriculturalLand
        fields = ["id", "land", "code", "name"]
        read_only_fields = ["id"]
