from rest_framework import serializers
from animal.models.vaccine import AnimalVaccine, VaccineStatus


class AnimalVaccineSerializer(serializers.ModelSerializer):
    animal_number = serializers.CharField(source="animal.animal_number", read_only=True)

    class Meta:
        model = AnimalVaccine
        fields = [
            "id",
            "animal",
            "animal_number",
            "name",
            "date_given",
            "valid_until",
            "status",
            "description",
            "image",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "animal_number"]
