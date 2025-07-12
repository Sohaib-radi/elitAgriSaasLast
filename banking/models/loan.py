from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import BaseModel, CreatedByMixin, FarmLinkedModel

from banking.models.bank import Bank

class Loan(BaseModel,FarmLinkedModel, CreatedByMixin):
    """
    Represents a loan taken by the farm from a bank with full management and tracking.
    """

    class RepaymentMethod(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        QUARTERLY = "quarterly", _("Quarterly")
        YEARLY = "yearly", _("Yearly")
        BULLET = "bullet", _("Bullet Payment")
        CUSTOM = "custom", _("Custom")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        CLOSED = "closed", _("Closed")
        DEFAULTED = "defaulted", _("Defaulted")

    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        related_name="loans",
        verbose_name=_("Bank"),
        help_text=_("Bank providing the loan")
    )
    loan_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Loan Number"),
        help_text=_("Unique identifier for the loan")
    )
    loan_name = models.CharField(
        max_length=255,
        verbose_name=_("Loan Name"),
        help_text=_("Name or title of the loan")
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Loan Amount"),
        help_text=_("Total amount of the loan")
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Interest Rate (%)"),
        help_text=_("Interest rate of the loan in percentage")
    )
    loan_duration = models.PositiveIntegerField(
        verbose_name=_("Loan Duration (months)"),
        help_text=_("Duration of the loan in months")
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_("Date when the loan starts")
    )
    end_date = models.DateField(
        verbose_name=_("End Date"),
        help_text=_("Date when the loan is due")
    )
    repayment_method = models.CharField(
        max_length=20,
        choices=RepaymentMethod.choices,
        default=RepaymentMethod.MONTHLY,
        verbose_name=_("Repayment Method"),
        help_text=_("Method of repayment for this loan")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("Status"),
        help_text=_("Current status of the loan")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Optional description for the loan"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Loan")
        verbose_name_plural = _("Loans")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.loan_name} ({self.loan_number}) - {self.amount}"
