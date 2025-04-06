from django.db import models
from ..models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Farm(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Farm Name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    location = models.CharField(max_length=255, blank=True, verbose_name=_("Location"))
    logo = models.ImageField(upload_to="farm_logos/", null=True, blank=True, verbose_name=_("Logo"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = "Farm"
        verbose_name_plural = "Farms"

    def __str__(self):
        return self.name
