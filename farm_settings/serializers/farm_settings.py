from rest_framework import serializers
from farm_settings.models import FarmSettings

class FarmSettingsSerializer(serializers.ModelSerializer):
    # Writable logo field (for upload)
    logo = serializers.ImageField(write_only=True, required=False)

    # Read-only logo URL from Farm
    logo_url = serializers.ImageField(source='farm.logo', read_only=True)
    slug = serializers.SlugField(source='farm.slug', read_only=True)

    class Meta:
        model = FarmSettings
        fields = "__all__"
        read_only_fields = ["logo_url", "slug"]

    def update(self, instance, validated_data):
        logo = validated_data.pop('logo', None)

        # Update settings normally
        instance = super().update(instance, validated_data)

        # Update the farm logo if provided
        if logo:
            instance.farm.logo = logo
            instance.farm.save()

        return instance