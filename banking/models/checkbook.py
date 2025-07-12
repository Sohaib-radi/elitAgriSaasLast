from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from banking.models.bank import Bank
from core.models.base import CreatedByMixin

class Checkbook(BaseModel, CreatedByMixin):
    """
    Represents a checkbook linked to a bank account.
    """

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Active")
        USED = "used", _("Used")
        CLOSED = "closed", _("Closed")

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="checkbooks",
        verbose_name=_("Bank"),
        help_text=_("Bank linked to this checkbook")
    )
    start_number = models.PositiveIntegerField(
        verbose_name=_("Start Check Number"),
        help_text=_("Starting check number in this checkbook")
    )
    end_number = models.PositiveIntegerField(
        verbose_name=_("End Check Number"),
        help_text=_("Ending check number in this checkbook")
    )
    issue_date = models.DateField(
        verbose_name=_("Issue Date"),
        help_text=_("Date when the checkbook was issued")
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        verbose_name=_("Status"),
        help_text=_("Current status of the checkbook")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        help_text=_("Optional note about this checkbook"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Checkbook")
        verbose_name_plural = _("Checkbooks")
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.bank.name} [{self.start_number} - {self.end_number}]"
