from django.db import models
from crop.models.agricultural_land import AgriculturalLand
from product_catalogue.models.product import Product
from core.models.base import FarmLinkedModel
from django.utils.translation import gettext_lazy as _

class LandStatusChoices(models.TextChoices):
    PLOUGHING = "ploughing", _("Ploughing")
    SOFTENING = "softening", _("Softening")
    PLANTED = "planted", _("Planted")
    UNUSABLE = "unusable", _("Unusable")
    TREATMENT = "treatment", _("Treatment")
    UNUSED = "unused", _("Unused")

class LandStatus(FarmLinkedModel):
    agricultural_land = models.ForeignKey(AgriculturalLand, on_delete=models.CASCADE, related_name="statuses", verbose_name=_("Agricultural Land"))
    status = models.CharField(max_length=30, choices=LandStatusChoices.choices, verbose_name=_("Land Status"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    product_used = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Product Used"))
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity Used"))
    date = models.DateField(verbose_name=_("Status Date"))

    class Meta:
        verbose_name = _("Land Status")
        verbose_name_plural = _("Land Statuses")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.agricultural_land.name} - {self.get_status_display()} ({self.date})"
