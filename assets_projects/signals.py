# in assets_projects/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProjectCost
from .models.project import Project  

@receiver([post_save, post_delete], sender=ProjectCost)
def update_project_total_costs(sender, instance, **kwargs):
    if instance.project:
        instance.project.update_total_costs()
