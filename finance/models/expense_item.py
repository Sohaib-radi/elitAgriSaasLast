from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from finance.models.expense_category import ExpenseCategory


class ExpenseItem(FarmLinkedModel):
    """
    💸 Represents a single expense entry under a category.
    Supports approval workflow and deducts from the monthly budget.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', _("Pending")
        APPROVED = 'approved', _("Approved")
        REJECTED = 'rejected', _("Rejected")

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name=_("Category")
    )
    code = models.CharField(
        max_length=20,
        verbose_name=_("Expense Number")
    )
    label = models.CharField(
        max_length=100,
        verbose_name=_("Label"),
        help_text=_("What the expense is (e.g., salary, service).")
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Amount")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPROVED,
        verbose_name=_("Status")
    )
    date = models.DateField(verbose_name=_("Date"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Expense Item")
        verbose_name_plural = _("Expense Items")
        ordering = ['-date']

    def __str__(self):
        return f"{self.label} - {self.amount} ({self.category.name})"
