from rest_framework import serializers
from animal.models.death import AnimalDeath, AnimalDeathImage
from animal.models.animal import Animal
from django.utils.translation import gettext_lazy as _

from animal.serializers.animal import AnimalSerializer

class AnimalDeathImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDeathImage
        fields = ["id", "image", "created_at"]
        read_only_fields = ["id", "created_at"]

class AnimalDeathSerializer(serializers.ModelSerializer):
    # Accepts ID during creation/updating
    animal = serializers.PrimaryKeyRelatedField(
        queryset=Animal.objects.all(),
        write_only=True
    )
    # Returns nested Animal details on retrieval
    animal_detail = AnimalSerializer(source='animal', read_only=True)

    images = AnimalDeathImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text=_("Upload one or more images showing the animal death."),
    )

    animal_number = serializers.CharField(source="animal.animal_number", read_only=True, help_text=_("Display animal number"))

    class Meta:
        model = AnimalDeath
        fields = [
            "id",
            "animal",             # For POST/PUT
            "animal_detail",      # For GET
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
        read_only_fields = ["id", "created_by", "created_at", "animal_number", "animal_detail", "images"]

    def validate_animal(self, animal):
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

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image in uploaded_images:
            AnimalDeathImage.objects.create(death=instance, image=image)

        return instance