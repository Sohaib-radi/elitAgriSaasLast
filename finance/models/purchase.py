from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from core.models.person import Person
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class PurchaseInvoice(FarmLinkedModel):
    """
    🧾 Represents a multi-item purchase invoice with structured financial data,
    supporting advanced invoice management and multi-item handling.
    """

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        CARD = "card", _("Credit Card")
        TRANSFER = "transfer", _("Bank Transfer")
        INSTALLMENT = "installment", _("Installment")
        OTHER = "other", _("Other")

    class Status(models.TextChoices):
        PAID = "paid", _("Paid")
        PENDING = "pending", _("Pending")
        OVERDUE = "overdue", _("Overdue")
        DRAFT = "draft", _("Draft")

    supplier = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="purchase_invoices",
        limit_choices_to={"type": "supplier"},
        verbose_name=_("Supplier"),
    )
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name=_("Invoice Number"))

    # Optional: Generic relation for advanced linking (e.g., related project or product group)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    linked_object = GenericForeignKey("content_type", "object_id")

    location = models.CharField(max_length=100,default="turkey", verbose_name=_("Transaction Location"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))

    date = models.DateField(verbose_name=_("Invoice Date"))
    delivery_date = models.DateField(blank=True, null=True, verbose_name=_("Delivery Date"))

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        verbose_name=_("Payment Method")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status")
    )

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Subtotal"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Discount"))
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Shipping"))
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Taxes"))
    vat = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("VAT (%)"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("Total Amount"))

    invoice_from = models.TextField(verbose_name=_("Invoice From"),default="Farm", help_text=_("Seller details for the invoice header"))
    invoice_to = models.TextField(verbose_name=_("Invoice To"),default="Farm", help_text=_("Buyer details for the invoice header"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Purchase Invoice")
        verbose_name_plural = _("Purchase Invoices")
        ordering = ["-date"]

    def __str__(self):
        return f"Purchase Invoice {self.invoice_number} - {self.supplier.name}"

    def update_totals(self):
        """
        Automatically calculate subtotal, taxes, and total_amount based on linked items.
        Should be called after adding/updating invoice items.
        """
        self.subtotal = sum(item.total for item in self.items.all())
        self.total_amount = self.subtotal - self.discount + self.shipping + self.taxes
        self.save(update_fields=["subtotal", "total_amount"])

    @property
    def paid_amount(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount


class PurchaseInvoiceItem(models.Model):
    """
    📦 Represents a line item within a PurchaseInvoice, supporting multi-item purchases.
    """

    invoice = models.ForeignKey(
        PurchaseInvoice,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Invoice"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    service = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Service"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Unit Price"))
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Total"), editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Purchase Invoice Item")
        verbose_name_plural = _("Purchase Invoice Items")

    def __str__(self):
        return f"{self.title} ({self.quantity} x {self.price})"

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)
        self.invoice.update_totals()


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
