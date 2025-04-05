# product_catalogue/models/personal_product.py

from django.db import models
from core.models.base import FarmLinkedModel
from django.utils.translation import gettext_lazy as _
from product_catalogue.models.project import Project

class PersonalProduct(FarmLinkedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="personal_products")
    product = models.ForeignKey("product_catalogue.Product", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "core.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_personal_products"
    )

    class Meta:
        verbose_name = _("Personal Product")
        verbose_name_plural = _("Personal Products")
        unique_together = ("project", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} → {self.project.name}"
