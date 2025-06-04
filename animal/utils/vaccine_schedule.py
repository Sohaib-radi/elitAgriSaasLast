from datetime import timedelta
from animal.models.recommendation import VaccineRecommendation
from animal.models.birth_vaccine import AnimalBirthVaccine
from animal.models.vaccine import AnimalVaccine, VaccineStatus
from django.utils import timezone

def generate_vaccine_plan_for_birth(birth, created_by=None):
    """
    Creates scheduled AnimalBirthVaccine entries for the birth record.
    """
    recommendations = VaccineRecommendation.objects.filter(species=birth.species)
    created = []

    for rec in recommendations:
        date_given = birth.birth_datetime.date() + timedelta(days=rec.recommended_age_days)

        # Prevent duplicates
        exists = AnimalBirthVaccine.objects.filter(
            birth=birth,
            name=rec.vaccine_name,
            date_given=date_given
        ).exists()

        if not exists:
            vaccine = AnimalBirthVaccine.objects.create(
                birth=birth,
                name=rec.vaccine_name,
                date_given=date_given,
                valid_until=date_given + timedelta(days=365),
                status=VaccineStatus.SCHEDULED,
                description=rec.description,
                created_by=created_by
            )
            created.append(vaccine)

    return created



def generate_vaccine_plan_for_animal(animal, created_by=None, is_purchased=False):
    """
    Creates scheduled AnimalVaccine entries for a real animal.
    Includes filters for species and whether the animal is newly purchased.
    """
    # Only include purchased-specific recommendations if applicable
    print("[DEBUG] Initial recs:", VaccineRecommendation.objects.filter(species=animal.species).count())
    print("[DEBUG] Purchased recs:", VaccineRecommendation.objects.filter(species=animal.species, applies_to_purchased=True).count())

    recommendations = VaccineRecommendation.objects.filter(species=animal.species)
    if is_purchased:
        recommendations = recommendations.filter(applies_to_purchased=True)

    created = []

    for rec in recommendations:
        date_given = animal.birth_date + timedelta(days=rec.recommended_age_days)

        # Optional: skip future vaccines if not needed
        if date_given > timezone.now().date():
            continue

        exists = AnimalVaccine.objects.filter(
            animal=animal,
            name=rec.vaccine_name,
            date_given=date_given
        ).exists()

        if not exists:
            vaccine = AnimalVaccine.objects.create(
                animal=animal,
                name=rec.vaccine_name,
                date_given=date_given,
                valid_until=date_given + timedelta(days=365),
                status=VaccineStatus.SCHEDULED,
                description=rec.description,
                created_by=created_by,
            )
            created.append(vaccine)

    # ✅ Log how many were created (for dev/testing)
    print(f"[INFO] Created {len(created)} vaccines for animal {animal.animal_number}")

    return created
