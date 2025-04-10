from django.db.models.signals import post_save
from django.dispatch import receiver
from product_catalogue.models.supplier import Supplier
from core.models.team import TeamMember
from core.models.person import Person
from finance.models.buyer import Buyer

@receiver(post_save, sender=Supplier)
def create_person_for_supplier(sender, instance, created, **kwargs):
    if created and not Person.objects.filter(supplier=instance).exists():
        Person.objects.create(
            name=instance.name,
            phone=instance.phone,
            address=instance.address,
            type="supplier",
            supplier=instance,
            farm=instance.farm,
            description="Auto-created from Supplier"
        )


@receiver(post_save, sender=TeamMember)
def create_person_for_teammember(sender, instance, created, **kwargs):
    if created and not Person.objects.filter(team_member=instance).exists():
        Person.objects.create(
            name=instance.user.full_name,
            phone=instance.user.phone,
            address="",
            type="staff",
            team_member=instance,
            farm=instance.farm,
            description="Auto-created from Team Member"
        )

@receiver(post_save, sender=Buyer)
def create_person_for_buyer(sender, instance, created, **kwargs):
    if created and not Person.objects.filter(name=instance.name, type="client").exists():
        Person.objects.create(
            name=instance.name,
            type="client",
            phone=instance.phone,
            address=instance.address,
            farm=instance.farm
        )