# product_catalogue/models/project.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import BaseModel
from core.models.base import FarmLinkedModel  


class Project(BaseModel, FarmLinkedModel):
    """
    Represents a project within a farm context (e.g., seasonal activity, production goal).
    """
    name = models.CharField(max_length=255, verbose_name=_("Project Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        unique_together = ("farm", "name")
        ordering = ["-start_date"]

    def __str__(self):
        return self.name
