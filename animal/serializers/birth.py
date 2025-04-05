from rest_framework import serializers
from animal.models.birth import AnimalBirth


class AnimalBirthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBirth
        fields = [
            "id",
            "farm",
            "list",
            "mother",
            "father",
            "animal_number",
            "international_number",
            "species",
            "gender",
            "birth_datetime",
            "status",
            "description",
            "moved_to_animals",
            "created_at",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "farm",
            "moved_to_animals",
            "created_at",
            "created_by",
        ]
