from rest_framework import serializers
from animal.models.animal import Animal
from animal.models.birth import AnimalBirth
from animal.models.vaccine import AnimalVaccine
from animal.utils.vaccine_schedule import generate_vaccine_plan_for_animal, generate_vaccine_plan_for_birth


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

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        validated_data["farm"] = user.active_farm
        validated_data["created_by"] = user

        birth = super().create(validated_data)

        # ✅ Generate vaccine plan for newborn before moving to Animal
        generate_vaccine_plan_for_birth(birth, created_by=user)

        return birth
    def update(self, instance, validated_data):
        request = self.context["request"]
        user = request.user

        was_moved = instance.moved_to_animals
        instance = super().update(instance, validated_data)

        if not was_moved and instance.moved_to_animals:
            # 1. Create real animal
            newborn = Animal.objects.create(
                animal_number=instance.animal_number,
                international_number=instance.international_number,
                species=instance.species,
                gender=instance.gender,
                birth_date=instance.birth_datetime.date(),
                status='healthy',
                farm=instance.farm,
                created_by=user,
            )

            print(f"[DEBUG] Animal created from birth: {newborn.animal_number}")

            # 2. Copy planned birth vaccines
            for planned in instance.planned_vaccines.all():
                AnimalVaccine.objects.create(
                    animal=newborn,
                    name=planned.name,
                    date_given=planned.date_given,
                    valid_until=planned.valid_until,
                    status=planned.status,
                    description=planned.description,
                    image=planned.image,
                    created_by=planned.created_by,
                )

            # 3. Generate any animal-specific vaccine recommendations (not from birth plan)
            generate_vaccine_plan_for_animal(
                newborn,
                created_by=user,
                is_purchased=False
            )

        return instance
