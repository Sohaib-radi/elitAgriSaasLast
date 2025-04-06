from django.core.management.base import BaseCommand
from core.models.permissions import Permission

PERMISSION_CODES = {
    "products": ["view", "manage"],
    "personal_products": ["view", "manage"],
    "projects": ["view", "manage"],
    "suppliers": ["view", "manage"], 
    "animals": ["view", "manage"],
    "animal_births": ["view", "manage"],
    "animal_deaths": ["view", "manage"],
    "custom_fields": ["view", "manage"],
    "team": ["view", "manage"],
    "roles": ["view", "manage"],
    "lands": ["view", "manage"],
    "land_purchases": ["view", "manage"],
    "wilayas": ["view", "manage"],
    "warehouses": ["view", "manage"],
    "warehouse_entries": ["view", "manage"],
    "warehouse_quantity_schedules": ["view", "manage"],
    "warehouse_reminders": ["view", "manage"],
    "crop": ["view", "manage"],

    # ✅ Finance module
    "expenses": ["view", "manage"],
    "receipts": ["view", "manage"],
    "payments": ["view", "manage"],
    "revenues": ["view", "manage"],
    "debts": ["view", "manage"],
    "invoices": ["view", "manage"],
    "subscriptions": ["view", "manage"],
    "finance_reports": ["view"],
}

#python manage.py sync_permissions
class Command(BaseCommand):
    help = "Sync permission codes to the database"

    def handle(self, *args, **kwargs):
        count = 0
        for module, actions in PERMISSION_CODES.items():
            for action in actions:
                code = f"{module}.{action}"
                label = f"{module.replace('_', ' ').title()} → {action.capitalize()}"
                obj, created = Permission.objects.get_or_create(code=code, defaults={"label": label})
                if created:
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"{count} permissions synced successfully."))
