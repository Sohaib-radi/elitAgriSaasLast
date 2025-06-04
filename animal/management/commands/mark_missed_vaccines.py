from django.core.management.base import BaseCommand
from animal.models.vaccine import AnimalVaccine, VaccineStatus
from django.utils import timezone

#  Command crone JOBE"0 2 * * * /path/to/your/venv/bin/python /path/to/project/manage.py mark_missed_vaccines"

class Command(BaseCommand):
    help = "Mark scheduled vaccines as missed if the given date has passed."

    def handle(self, *args, **options):
        today = timezone.now().date()
        vaccines = AnimalVaccine.objects.filter(
            status=VaccineStatus.SCHEDULED,
            date_given__lt=today
        )
        count = vaccines.update(status=VaccineStatus.MISSED)
        self.stdout.write(self.style.SUCCESS(f"{count} vaccines marked as missed."))
