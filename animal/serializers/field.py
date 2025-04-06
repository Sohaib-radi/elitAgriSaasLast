from rest_framework import serializers
from animal.models.field import CustomListField, FieldType


class CustomListFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomListField
        fields = [
            "id",
            "list",
            "name",
            "field_type",
            "required",
            "options",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]
