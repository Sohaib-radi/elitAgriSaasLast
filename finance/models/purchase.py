from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from core.models.person import Person
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class PurchaseInvoice(FarmLinkedModel):
    """
    🧾 Represents a purchase invoice (single transaction for a product or asset)
    """

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        BANK_TRANSFER = "bank_transfer", _("Bank Transfer")
        INSTALLMENT = "installment", _("Installment")
        OTHER = "other", _("Other")

    supplier = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "supplier"},
        related_name="purchase_invoices",
        verbose_name=_("Supplier")
    )
    invoice_number = models.CharField(max_length=100, verbose_name=_("Invoice Number"))
    
    product_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    product_object_id = models.PositiveIntegerField()
    product = GenericForeignKey('product_content_type', 'product_object_id')

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total Amount"))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Unit Price"))

    payment_method = models.CharField(max_length=50, choices=PaymentMethod.choices, verbose_name=_("Payment Method"))
    delivery_date = models.DateField(blank=True, null=True, verbose_name=_("Delivery Date"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Purchase Invoice")
        verbose_name_plural = _("Purchase Invoices")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name}"

    @property
    def paid_amount(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount

class PurchasePayment(models.Model):
    """
    💰 Represents a partial or full payment made for a purchase invoice
    """

    invoice = models.ForeignKey(
        "finance.PurchaseInvoice",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Invoice")
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Amount Paid"))
    date = models.DateField(verbose_name=_("Payment Date"))
    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Purchase Payment")
        verbose_name_plural = _("Purchase Payments")
        ordering = ["-date"]

    def __str__(self):
        return f"Payment of {self.amount} for {self.invoice.invoice_number}"


class PurchaseAttachment(models.Model):
    invoice = models.ForeignKey(
        "finance.PurchaseInvoice",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Invoice"),
    )
    file = models.FileField(
        upload_to="purchases/attachments/",
        verbose_name=_("Attachment File"),
        help_text=_("PDF, image, or document related to the purchase.")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Purchase Attachment")
        verbose_name_plural = _("Purchase Attachments")

    def __str__(self):
        return f"{self.file.name}"
