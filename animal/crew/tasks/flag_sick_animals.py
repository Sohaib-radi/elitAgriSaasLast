from crewai import Task
from django.utils import timezone
from animal.models import Animal
from animal.models import VaccinationRecord
from datetime import timedelta

def flag_sick_animals(agent):
    def _execute_health_scan():
        today = timezone.now().date()
        overdue_vaccinations = []
        health_alerts = []

        # Step 1: Check for overdue vaccinations
        overdue_records = VaccinationRecord.objects.filter(valid_until__lt=today)
        overdue_animal_ids = set(overdue_records.values_list("animal_id", flat=True))
        for animal_id in overdue_animal_ids:
            animal = Animal.objects.filter(id=animal_id).first()
            if animal:
                overdue_vaccinations.append(f"{animal.species} #{animal.id} - {animal.name}")

        # Step 2: Flag health issues (abnormal temperature or missing recent health check)
        sick_animals = Animal.objects.filter(is_active=True).filter(
            temperature__gt=39.5
        ) | Animal.objects.filter(
            last_health_check__lt=today - timedelta(days=30)
        )

        for animal in sick_animals:
            issue = "high temp" if animal.temperature and animal.temperature > 39.5 else "no health check"
            health_alerts.append(f"{animal.species} #{animal.id} - {animal.name} ({issue})")

        return {
            "status": "analyzed",
            "overdue_vaccinations": overdue_vaccinations,
            "health_alerts": health_alerts,
            "message": "Scan complete. Report generated with flagged health issues and vaccine alerts."
        }

    return Task(
        description="Scan animal health data and vaccination records to flag overdue vaccines and detect any abnormal health signs.",
        expected_output="Detailed report of animals with overdue vaccinations or abnormal health indicators.",
        agent=agent.get(),
        tools=[_execute_health_scan]
    )
