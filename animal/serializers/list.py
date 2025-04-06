from rest_framework import serializers
from animal.models.list import AnimalList


class AnimalListSerializer(serializers.ModelSerializer):
    
    def validate_name(self, value):
        farm = self.context["request"].user.active_farm
        if AnimalList.objects.filter(farm=farm, name=value).exists():
            raise serializers.ValidationError("This list name already exists for your farm.")
        return value
    class Meta:
        model = AnimalList
        fields = [
            "id",
            "name",
            "image",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
