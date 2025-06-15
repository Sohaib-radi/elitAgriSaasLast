# product_catalogue/models/supplier.py

from django.db import models
from core.models.base import FarmLinkedModel
from django.utils.translation import gettext_lazy as _

class SupplierList(FarmLinkedModel):
    name = models.CharField(max_length=255, verbose_name=_("List Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Supplier List")
        verbose_name_plural = _("Supplier Lists")
        unique_together = ("farm", "name")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

