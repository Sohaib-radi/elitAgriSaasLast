from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from banking.models.bank import Bank
from core.models.base import CreatedByMixin

class BankCard(BaseModel, CreatedByMixin):
    """
    Represents a card (credit, debit, prepaid, or checkbook) linked to a bank account.
    """

    class CardTypeChoices(models.TextChoices):
        CREDIT = "credit", _("Credit Card")
        DEBIT = "debit", _("Debit Card")
        PREPAID = "prepaid", _("Prepaid Card")
        CHECKBOOK = "checkbook", _("Checkbook")

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Active")
        BLOCKED = "blocked", _("Blocked")
        EXPIRED = "expired", _("Expired")

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name=_("Bank"),
        help_text=_("Bank this card is linked to")
    )

    
    card_type = models.CharField(
        max_length=20,
        choices=CardTypeChoices.choices,
        verbose_name=_("Card Type"),
        help_text=_("Type of the card")
    )
    card_number = models.CharField(
        max_length=50,
        verbose_name=_("Card Number"),
        help_text=_("Card or checkbook number"),
        unique=True
    )
    holder_name = models.CharField(
        max_length=255,
        verbose_name=_("Holder Name"),
        help_text=_("Name on the card"),
    )
    issue_date = models.DateField(
        verbose_name=_("Issue Date"),
        help_text=_("Date when the card was issued")
    )
    expiry_date = models.DateField(
        verbose_name=_("Expiry Date"),
        help_text=_("Card expiry date"),
        blank=True,
        null=True
    )
    card_limit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Card Limit"),
        help_text=_("Limit of the card if applicable"),
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        verbose_name=_("Status"),
        help_text=_("Current status of the card")
    )
    note = models.TextField(
        verbose_name=_("Note"),
        help_text=_("Optional note about this card"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Bank Card")
        verbose_name_plural = _("Bank Cards")
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.card_type} - {self.card_number}"
