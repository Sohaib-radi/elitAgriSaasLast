from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from banking.models.checkbook import Checkbook
from banking.models.bank_transaction import BankTransaction
from core.models.base import CreatedByMixin

class Check(BaseModel, CreatedByMixin):
    """
    Tracks individual checks (incoming and outgoing) linked to a checkbook.
    """

    class StatusChoices(models.TextChoices):
        ISSUED = "issued", _("Issued")
        CLEARED = "cleared", _("Cleared")
        BOUNCED = "bounced", _("Bounced")
        CANCELLED = "cancelled", _("Cancelled")

    class PaymentStatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")

    class DirectionChoices(models.TextChoices):
        INCOMING = "incoming", _("Incoming")
        OUTGOING = "outgoing", _("Outgoing")

    checkbook = models.ForeignKey(
        Checkbook,
        on_delete=models.CASCADE,
        related_name="checks",
        verbose_name=_("Checkbook"),
        help_text=_("Checkbook this check belongs to")
    )
    check_number = models.PositiveIntegerField(
        verbose_name=_("Check Number"),
        help_text=_("Unique number of the check")
    )
    issue_date = models.DateField(
        verbose_name=_("Issue Date"),
        help_text=_("Date when the check was issued")
    )
    due_date = models.DateField(
        verbose_name=_("Due Date"),
        help_text=_("Date when the check should be paid")
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Amount"),
        help_text=_("Amount of the check")
    )
    beneficiary_name = models.CharField(
        max_length=255,
        verbose_name=_("Beneficiary Name"),
        help_text=_("Name of the person or entity receiving the check")
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ISSUED,
        verbose_name=_("Status"),
        help_text=_("Current status of the check")
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
        verbose_name=_("Payment Status"),
        help_text=_("Payment status of the check")
    )
    transaction = models.ForeignKey(
        BankTransaction,
        on_delete=models.SET_NULL,
        related_name="checks",
        verbose_name=_("Linked Transaction"),
        help_text=_("Transaction linked to this check, if applicable"),
        blank=True,
        null=True
    )
    direction = models.CharField(
        max_length=10,
        choices=DirectionChoices.choices,
        default=DirectionChoices.OUTGOING,
        verbose_name=_("Direction"),
        help_text=_("Indicates if the check is incoming or outgoing")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        help_text=_("Optional note about this check"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Check")
        verbose_name_plural = _("Checks")
        ordering = ["-due_date"]

    def __str__(self):
        return f"{self.check_number} - {self.beneficiary_name} - {self.amount}"
