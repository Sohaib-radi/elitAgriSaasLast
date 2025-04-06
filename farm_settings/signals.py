from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Farm
from farm_settings.models import FarmSettings

@receiver(post_save, sender=Farm)
def create_farm_settings(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "settings"):
        FarmSettings.objects.create(farm=instance)