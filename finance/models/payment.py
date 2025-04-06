from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from core.models.person import Person


class Payment(FarmLinkedModel):
    """
    💸 Represents a payment voucher — money paid to a supplier, staff, or other person.
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Recipient"),
        help_text=_("The person receiving the payment.")
    )
    payment_number = models.CharField(max_length=50, verbose_name=_("Payment Number"))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Amount"))
    date = models.DateField(verbose_name=_("Date"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    accountant_signature = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Accountant Signature"))
    recipient_signature = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Recipient Signature"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Payment Voucher")
        verbose_name_plural = _("Payment Vouchers")
        ordering = ["-date"]

    def __str__(self):
        return f"Payment {self.payment_number} - {self.person.name}"
