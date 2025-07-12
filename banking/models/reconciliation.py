from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import BaseModel, CreatedByMixin
from banking.models.bank_transaction import BankTransaction
from banking.models.loan_payment import LoanPayment
from banking.models.check import Check

class ReconciliationStatus(models.TextChoices):
    UNMATCHED = "unmatched", _("Unmatched")
    PARTIALLY_MATCHED = "partially_matched", _("Partially Matched")
    FULLY_MATCHED = "fully_matched", _("Fully Matched")

class Reconciliation(BaseModel, CreatedByMixin):
    """
    Tracks reconciliation between a bank transaction and internal financial records.
    """

    bank_transaction = models.ForeignKey(
        BankTransaction,
        on_delete=models.CASCADE,
        related_name="reconciliations",
        verbose_name=_("Bank Transaction"),
        help_text=_("Bank transaction being reconciled")
    )
    loan_payment = models.ForeignKey(
        LoanPayment,
        on_delete=models.SET_NULL,
        related_name="reconciliations",
        verbose_name=_("Loan Payment"),
        help_text=_("Linked loan payment, if applicable"),
        null=True,
        blank=True
    )
    linked_check = models.ForeignKey(
        Check,
        on_delete=models.SET_NULL,
        related_name="reconciliations",
        verbose_name=_("Linked Check"),
        help_text=_("Linked check, if applicable"),
        null=True,
        blank=True
    )
    reconciled_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Reconciled Amount"),
        help_text=_("Amount reconciled from the bank transaction")
    )
    status = models.CharField(
        max_length=20,
        choices=ReconciliationStatus.choices,
        default=ReconciliationStatus.UNMATCHED,
        verbose_name=_("Reconciliation Status"),
        help_text=_("Status of the reconciliation")
    )
    reconciliation_date = models.DateField(
        auto_now_add=True,
        verbose_name=_("Reconciliation Date"),
        help_text=_("Date when the reconciliation was performed")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        help_text=_("Optional note about this reconciliation"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Reconciliation")
        verbose_name_plural = _("Reconciliations")
        ordering = ["-reconciliation_date"]

    def __str__(self):
        return f"{self.bank_transaction} - {self.reconciled_amount} ({self.get_status_display()})"
