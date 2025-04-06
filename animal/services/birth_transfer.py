from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from animal.models import Animal

def move_birth_to_animal(birth):
    # Check if already moved
    if birth.moved_to_animals:
        raise ValidationError(_("This birth has already been moved to animals."))

    # Check for duplicate animal_number in same farm
    if Animal.objects.filter(farm=birth.farm, animal_number=birth.animal_number).exists():
        raise ValidationError(_("Animal with this number already exists in the farm."))

    # Create new Animal from Birth
    animal = Animal.objects.create(
        farm=birth.farm,
        list=birth.list,
        mother=birth.mother,
        father=birth.father,
        animal_number=birth.animal_number,
        international_number=birth.international_number,
        name=None,
        species=birth.species,
        breed=None,
        gender=birth.gender,
        birth_date=birth.birth_datetime.date(),
        status=birth.status,
        description=birth.description,
        created_by=birth.created_by,
    )

    # ✅ Mark as moved
    birth.moved_to_animals = True
    birth.save()

    return animal
