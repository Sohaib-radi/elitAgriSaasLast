from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel

class Buyer(FarmLinkedModel):
    """
    🧾 Represents a buyer (client) for sales invoices.
    """
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    buyer_number = models.CharField(max_length=50, verbose_name=_("Buyer Number"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Buyer")
        verbose_name_plural = _("Buyers")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.buyer_number}"
