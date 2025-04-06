from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel


class ExpenseCategory(FarmLinkedModel):
    """
    Represents a categorized expense list (e.g., salaries, fuel, feed).
    Supports monthly budget tracking, optional image, and type classification.
    """

    class CategoryType(models.TextChoices):
        AGRICULTURE = 'agriculture', _("Agriculture")
        ANIMAL = 'animal', _("Animal")
        WAREHOUSE = 'warehouse', _("Warehouse")
        OTHER = 'other', _("Other")

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Title of the expense list.")
    )
    code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Code"),
        help_text=_("Optional reference code or number.")
    )
    type = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        default=CategoryType.OTHER,
        verbose_name=_("Type")
    )
    monthly_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Monthly Budget")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )
    image = models.ImageField(
        upload_to="expenses/categories/",
        blank=True,
        null=True,
        verbose_name=_("Image")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Expense Category")
        verbose_name_plural = _("Expense Categories")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.farm.name})"
