from django.db import models
from crop.models.agricultural_land import AgriculturalLand
from core.models.base import FarmLinkedModel
from django.utils.translation import gettext_lazy as _

class CropStatusChoices(models.TextChoices):
    PLANNED = "planned", _("Planned")
    GROWING = "growing", _("Growing")
    HARVESTED = "harvested", _("Harvested")
    FAILED = "failed", _("Failed")
    SOLD = "sold", _("Sold")

class UsageChoices(models.TextChoices):
    FOR_SALE = "for_sale", _("For Sale")
    FOR_FEED = "for_feed", _("Animal Feed")

class UnitChoices(models.TextChoices):
    KG = "kg", _("Kilogram")
    TON = "ton", _("Ton")
    SACK = "sack", _("Sack")

class Crop(FarmLinkedModel):
    agricultural_land = models.ForeignKey(AgriculturalLand, on_delete=models.CASCADE, related_name="crops", verbose_name=_("Agricultural Land"))
    crop_type = models.CharField(max_length=100, verbose_name=_("Crop Type"))
    status = models.CharField(max_length=20, choices=CropStatusChoices.choices, verbose_name=_("Crop Status"))
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity"))
    unit = models.CharField(max_length=10, choices=UnitChoices.choices, verbose_name=_("Unit"))
    usage = models.CharField(max_length=20, choices=UsageChoices.choices, verbose_name=_("Usage"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    date = models.DateField(verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Crop")
        verbose_name_plural = _("Crops")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.crop_type} - {self.quantity} {self.unit} ({self.get_status_display()})"
