from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import BaseModel, CreatedByMixin, FarmLinkedModel
from banking.models.loan import Loan

class LoanPayment(BaseModel,FarmLinkedModel,CreatedByMixin):
    """
    Tracks individual payments made for a loan, including principal and interest portions.
    """

    class PaymentMethodChoices(models.TextChoices):
        CASH = "cash", _("Cash")
        BANK_TRANSFER = "bank_transfer", _("Bank Transfer")
        CHECK = "check", _("Check")
        OTHER = "other", _("Other")

    class StatusChoices(models.TextChoices):
        CONFIRMED = "confirmed", _("Confirmed")
        PENDING = "pending", _("Pending")
        REJECTED = "rejected", _("Rejected")
        PAID = "paid", _("Paid")

    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Loan"),
        help_text=_("Loan related to this payment")
    )
    payment_date = models.DateField(
        verbose_name=_("Payment Date"),
        help_text=_("Date of this payment")
    )
    amount_paid = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Total Amount Paid"),
        help_text=_("Total amount paid in this payment")
    )
    principal_paid = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Principal Paid"),
        help_text=_("Principal portion of the payment")
    )
    interest_paid = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Interest Paid"),
        help_text=_("Interest portion of the payment")
    )
    remaining_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Remaining Balance"),
        help_text=_("Remaining balance of the loan after this payment")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.BANK_TRANSFER,
        verbose_name=_("Payment Method"),
        help_text=_("Method used for this payment")
    )
    payment_reference = models.CharField(
        max_length=255,
        verbose_name=_("Payment Reference"),
        help_text=_("Reference or receipt number for this payment"),
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.CONFIRMED,
        verbose_name=_("Status"),
        help_text=_("Status of the payment")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        help_text=_("Optional note for this payment"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Loan Payment")
        verbose_name_plural = _("Loan Payments")
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.loan.loan_name} - {self.amount_paid} on {self.payment_date}"
