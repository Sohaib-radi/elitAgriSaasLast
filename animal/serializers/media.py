from rest_framework import serializers
from animal.models.media import AnimalImage


class AnimalImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ["id", "image", "caption"]
        extra_kwargs = {
            "caption": {"required": False},
        }
