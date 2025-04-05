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
    
    def validate(self, data):
        data = super().validate(data)
        custom_data = self.initial_data.get("custom_fields", {})
        animal_list = data.get("list")

        if animal_list:
            for field in animal_list.custom_fields.all():
                val = custom_data.get(field.name)
                if field.required and (val in [None, "", []]):
                    raise serializers.ValidationError({f"custom_fields.{field.name}": _("This field is required.")})

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

        # Save custom fields
        from animal.models.field_value import AnimalCustomFieldValue
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


    def create_many(self, validated_data_list):
        farm = self.context["request"].user.active_farm
        user = self.context["request"].user
        for item in validated_data_list:
            item["farm"] = farm
            item["created_by"] = user
        return Animal.objects.bulk_create([Animal(**item) for item in validated_data_list])

    def save(self, **kwargs):
        if isinstance(self.validated_data, list):
            self.instance = self.create_many(self.validated_data)
        else:
            self.instance = self.create(self.validated_data)
        return self.instance
