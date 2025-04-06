from datetime import timedelta
from animal.models.recommendation import VaccineRecommendation
from animal.models.birth import AnimalBirth

def suggest_vaccines_for_birth(birth: AnimalBirth):
    """
    Based on birth species, return a list of vaccine suggestions.
    """
    recommendations = VaccineRecommendation.objects.filter(species=birth.species)
    suggestions = []

    for rec in recommendations:
        due_date = birth.birth_datetime.date() + timedelta(days=rec.recommended_age_days)
        suggestions.append({
            "animal_birth_id": birth.id,
            "vaccine": rec.vaccine_name,
            "due_date": due_date,
            "repeat_every_days": rec.repeat_interval_days,
            "description": rec.description,
        })

    return suggestions
