from rest_framework import serializers
from animal.models.death import AnimalDeath, AnimalDeathImage
from animal.models.animal import Animal
from django.utils.translation import gettext_lazy as _


class AnimalDeathImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDeathImage
        fields = ["id", "image", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class AnimalDeathSerializer(serializers.ModelSerializer):
    images = AnimalDeathImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text=_("One or more images showing the animal death"),
    )
    animal_number = serializers.CharField(source="animal.animal_number", read_only=True, help_text=_("Display animal number"))

    class Meta:
        model = AnimalDeath
        fields = [
            "id",
            "animal",
            "animal_number",
            "death_datetime",
            "reason",
            "description",
            "status",
            "images",
            "uploaded_images",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "animal_number"]

    def validate_animal(self, animal):
        """Ensure the animal belongs to the user's active farm"""
        request = self.context["request"]
        if animal.farm != request.user.active_farm:
            raise serializers.ValidationError(_("This animal does not belong to your active farm."))
        return animal

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        death = AnimalDeath.objects.create(**validated_data)

        for image in uploaded_images:
            AnimalDeathImage.objects.create(death=death, image=image)

        return death
