from django.db import models
from django.utils.translation import gettext_lazy as _
from  core.models.base import BaseModel, CreatedByMixin, FarmLinkedModel
from farm_settings.models.currency import Currency  

class Bank(BaseModel,FarmLinkedModel, CreatedByMixin):
    """
    Represents a bank where the farm holds accounts for transactions.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_("Bank Name"),
        help_text=_("Name of the bank")
    )
    bank_number = models.CharField(
        max_length=100,
        verbose_name=_("Bank Number"),
        help_text=_("Internal bank number"),
        unique=True
    )
    
    branch = models.CharField(
        max_length=255,
        verbose_name=_("Branch"),
        help_text=_("Branch of the bank"),
        blank=True,
        null=True
    )
    account_number = models.CharField(
        max_length=100,
        verbose_name=_("Account Number"),
        help_text=_("Bank account number"),
        unique=True
    )
    iban = models.CharField(
        max_length=34,
        verbose_name=_("IBAN"),
        help_text=_("International Bank Account Number"),
        blank=True,
        null=True
    )
    swift_code = models.CharField(
        max_length=11,
        verbose_name=_("SWIFT Code"),
        help_text=_("Bank SWIFT code"),
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_("Address"),
        help_text=_("Address of the bank"),
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=50,
        verbose_name=_("Phone Number"),
        help_text=_("Phone number of the bank"),
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("Email address of the bank"),
        blank=True,
        null=True
    )
    main_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        verbose_name=_("Main Currency"),
        help_text=_("Main currency used by the bank"),
        related_name="banks"
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Optional description about the bank"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.bank_number}"
