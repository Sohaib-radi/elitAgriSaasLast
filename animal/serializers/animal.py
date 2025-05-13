from datetime import date
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from animal.models.animal import Animal
from animal.models.media import AnimalImage
from animal.models.list import AnimalList
from animal.models.field_value import AnimalCustomFieldValue
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ["id", "image", "caption", "created_at"]
        read_only_fields = ["id", "created_at"]

# NB :  the custom field creation not work on bluk insert

class AnimalSerializer(serializers.ModelSerializer):
    images = AnimalImageSerializer(many=True, read_only=True)
    custom_fields = serializers.JSONField(write_only=True, required=False)
    list_name = serializers.CharField(source="list.name", read_only=True)
    custom_field_values = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Animal
        fields = [
            "id",
            "animal_number",
            "international_number",
            "name",
            "species",
            "breed",
            "gender",
            "birth_date",
            "status",
            "mother",
            "father",
            "description",
            "is_active",
            "list",
            "list_name",
            "images",
            "created_by",
            "farm",
            "created_at",
            "custom_fields",
            "custom_field_values"
        ]
        read_only_fields = [
            "id", "created_at", "created_by", "farm", "images", "list_name"
        ]

    def get_custom_field_values(self, obj):
        values = AnimalCustomFieldValue.objects.filter(animal=obj)
        return {val.field.name: val.value for val in values}

    def validate_animal_number(self, value):
        farm = self.context["request"].user.active_farm
        qs = Animal.objects.filter(animal_number=value, farm=farm)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(_("An animal with this number already exists in this farm."))

        return value

    def validate(self, data):
        data = super().validate(data)

        # ✅ Custom field logic
        custom_data = self.initial_data.get("custom_fields", {})
        animal_list = data.get("list")

        if animal_list:
            for field in animal_list.custom_fields.all():
                val = custom_data.get(field.name)
                if field.required and (val in [None, "", []]):
                    raise serializers.ValidationError({
                        f"custom_fields.{field.name}": _("This field is required.")
                    })

        data["custom_fields"] = custom_data
        return data

    def create(self, validated_data):
        farm = self.context["request"].user.active_farm
        user = self.context["request"].user
        custom_fields = validated_data.pop("custom_fields", {})

        try:
            animal = Animal.objects.create(
                **validated_data,
                farm=farm,
                created_by=user,
            )
        except IntegrityError:
            raise ValidationError({
                "animal_number": _("An animal with this number already exists in this farm.")
            })

        for field in animal.list.custom_fields.all():
            value = custom_fields.get(field.name)
            if value is not None:
                AnimalCustomFieldValue.objects.create(
                    animal=animal,
                    field=field,
                    value=value,
                    created_by=user,
                )

        return animal
class AnimalStatusSerializer(serializers.Serializer):
    key = serializers.CharField()
    label = serializers.CharField()

class SimpleAnimalSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ["id", "animal_number", "species", "gender", "age", "profile_image"]

    def get_profile_image(self, obj):
        first_image = obj.images.first()
        return first_image.image.url if first_image else None

    def get_age(self, obj):
        if not obj.birth_date:
            return None
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImage
        fields = ["id", "image", "caption", "created_at"]

class AnimalDetailSerializer(serializers.ModelSerializer):
    images = AnimalImageSerializer(many=True, read_only=True)
    list_name = serializers.CharField(source="list.name", read_only=True)
    custom_field_values = serializers.SerializerMethodField()
    
    # ✅ force DRF to use nested serializer
    mother = SimpleAnimalSerializer(read_only=True)
    father = SimpleAnimalSerializer(read_only=True)
    def get_mother(self, obj):
        return {"id": 999, "animal_number": "TEST123", "species": "test", "gender": "female"}
    class Meta:
        model = Animal
        fields = [
            "id",
            "animal_number",
            "international_number",
            "name",
            "species",
            "breed",
            "gender",
            "birth_date",
            "status",
            "description",
            "is_active",
            "list",
            "list_name",
            "images",
            "created_by",
            "farm",
            "created_at",
            "custom_field_values",
            "mother",     # ✅ must be here
            "father",     # ✅ must be here
        ]
        read_only_fields = fields

    def get_custom_field_values(self, obj):
        values = AnimalCustomFieldValue.objects.filter(animal=obj)
        return {val.field.name: val.value for val in values}
    def to_representation(self, instance):
        print("✅ Using AnimalDetailSerializer")
        return super().to_representation(instance)