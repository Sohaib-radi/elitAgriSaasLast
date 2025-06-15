from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from product_catalogue.models.supplier_list import SupplierList

class Supplier(FarmLinkedModel):
    list = models.ForeignKey(SupplierList, on_delete=models.SET_NULL, null=True, blank=True, related_name="suppliers")
    product = models.ForeignKey("product_catalogue.Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="suppliers")
    
    supplier_name = models.CharField(max_length=255, verbose_name=_("Supplier Name"))
    company_name = models.CharField(max_length=255, blank=True, verbose_name=_("Company Name"))
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    product_type = models.CharField(max_length=255, verbose_name=_("Product Type"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to="supplier_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.supplier_name} - {self.product.name if self.product else 'N/A'}"
