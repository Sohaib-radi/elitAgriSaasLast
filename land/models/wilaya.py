from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin


class Wilaya(TimeStampedModel, CreatedByMixin):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Wilaya Name"))
    code = models.CharField(max_length=20, unique=False, default='TR', verbose_name=_("Wilaya Code"))

    class Meta:
        verbose_name = _("Wilaya")
        verbose_name_plural = _("Wilayas")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return self.name
