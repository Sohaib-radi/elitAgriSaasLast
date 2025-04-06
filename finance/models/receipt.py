from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from core.models.person import Person


class Receipt(FarmLinkedModel):
    """
    Represents a receipt voucher — income received from a person (client, buyer, etc.)
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="receipts",
        verbose_name=_("Payer"),
        help_text=_("The person making the payment.")
    )
    receipt_number = models.CharField(max_length=50, verbose_name=_("Receipt Number"))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Amount"))
    date = models.DateField(verbose_name=_("Date"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    accountant_signature = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Accountant Signature"))
    recipient_signature = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Recipient Signature"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Receipt Voucher")
        verbose_name_plural = _("Receipt Vouchers")
        ordering = ["-date"]

    def __str__(self):
        return f"Receipt {self.receipt_number} - {self.person.name}"
