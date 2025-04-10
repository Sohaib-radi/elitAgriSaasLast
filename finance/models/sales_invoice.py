from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from finance.models.buyer import Buyer
from core.models.person import Person

class SalesInvoice(FarmLinkedModel):
    """
    🧾 Represents a generic sales transaction linked to any object (land, crop, animal, birth, etc.)
    """

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        CARD = "card", _("Credit Card")
        TRANSFER = "transfer", _("Bank Transfer")
        OTHER = "other", _("Other")

    buyer = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="sales_invoices",
        limit_choices_to={"type": "client"}, 
        verbose_name=_("Buyer")
    )
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name=_("Invoice Number"))

    # ✅ Generic relation to product (can be land, crop, animal, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    product_object = GenericForeignKey("content_type", "object_id")

    location = models.CharField(max_length=100, verbose_name=_("Transaction Location"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    date = models.DateField(verbose_name=_("Sale Date"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Unit Price"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total Amount"))
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, verbose_name=_("Payment Method"))
    delivery_date = models.DateField(blank=True, null=True, verbose_name=_("Delivery Date"))
    vat = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("VAT (%)"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Sales Invoice")
        verbose_name_plural = _("Sales Invoices")
        ordering = ["-date"]

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.buyer.name}"
