from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import BaseModel, CreatedByMixin
from banking.models.bank import Bank
from banking.models.loan import Loan

class BankTransaction(BaseModel, CreatedByMixin):
    """
    Tracks all transactions within a bank account.
    """

    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", _("Deposit")
        WITHDRAWAL = "withdrawal", _("Withdrawal")
        TRANSFER = "transfer", _("Transfer")
        FEE = "fee", _("Fee")
        INTEREST = "interest", _("Interest")
        LOAN_PAYMENT = "loan_payment", _("Loan Payment")
        LOAN_DISBURSEMENT = "loan_disbursement", _("Loan Disbursement")

    class PaymentMethodChoices(models.TextChoices):
        CASH = "cash", _("Cash")
        BANK_TRANSFER = "bank_transfer", _("Bank Transfer")
        CHECK = "check", _("Check")
        OTHER = "other", _("Other")

    class StatusChoices(models.TextChoices):
        CONFIRMED = "confirmed", _("Confirmed")
        PENDING = "pending", _("Pending")
        REJECTED = "rejected", _("Rejected")

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("Bank"),
        help_text=_("Bank where the transaction occurred")
    )
    transaction_date = models.DateField(
        verbose_name=_("Transaction Date"),
        help_text=_("Date of the transaction")
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Amount"),
        help_text=_("Transaction amount")
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        verbose_name=_("Transaction Type"),
        help_text=_("Type of transaction")
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        verbose_name=_("Payment Method"),
        help_text=_("Payment method used for this transaction")
    )
    reference = models.CharField(
        max_length=255,
        verbose_name=_("Reference"),
        help_text=_("Transaction reference or description"),
        blank=True,
        null=True
    )
    loan = models.ForeignKey(
        Loan,
        on_delete=models.SET_NULL,
        related_name="transactions",
        verbose_name=_("Related Loan"),
        help_text=_("Related loan if applicable"),
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.CONFIRMED,
        verbose_name=_("Status"),
        help_text=_("Status of the transaction")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        help_text=_("Optional note for this transaction"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Bank Transaction")
        verbose_name_plural = _("Bank Transactions")
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.transaction_date}"
