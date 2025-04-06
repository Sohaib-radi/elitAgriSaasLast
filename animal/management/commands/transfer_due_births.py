from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from animal.models.birth import AnimalBirth
from animal.services.birth_transfer import move_birth_to_animal
from core.models.audit import UserLog
from core.constants.log_actions import LogActions


class Command(BaseCommand):
    help = "Automatically transfer births older than 9 months to Animal list"

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=270)  # 9 months ≈ 270 days

        due_births = AnimalBirth.objects.filter(
            moved_to_animals=False,
            birth_datetime__lte=cutoff_date
        )

        total = due_births.count()
        if total == 0:
            self.stdout.write("✅ No births are due for transfer.")
            return

        self.stdout.write(f"🔄 Transferring {total} birth(s) to animal list...\n")

        for birth in due_births:
            try:
                animal = move_birth_to_animal(birth)
                UserLog.objects.create(
                action=LogActions.AUTO_BIRTH_TRANSFER,
                description=f"Birth {birth.animal_number} auto-transferred to animal list.",
                farm=animal.farm,
                created_by=None
                )

                self.stdout.write(f"✅ Moved: {animal.animal_number} ({animal.species})")
            except Exception as e:
                self.stdout.write(f"❌ Failed to move birth ID {birth.id}: {str(e)}")

        self.stdout.write("🎯 Transfer complete.")
