from rest_framework import serializers
from farm_settings.models import FarmSettings

class FarmSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmSettings
        fields = "__all__"
