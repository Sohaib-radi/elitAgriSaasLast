from django.db import models
from core.models.base import FarmLinkedModel
from land.models import Land
from django.utils.translation import gettext_lazy as _

class AgriculturalLand(FarmLinkedModel):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="agricultural_lands", verbose_name=_("Linked Land"))
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Agricultural Land Code"))
    name = models.CharField(max_length=255, verbose_name=_("Land Name"))

    class Meta:
        verbose_name = _("Agricultural Land")
        verbose_name_plural = _("Agricultural Lands")
        indexes = [models.Index(fields=["code", "farm"])]

    def __str__(self):
        return f"{self.name} ({self.code})"
