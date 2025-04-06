from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel


class Person(FarmLinkedModel):
    """
    🧍 Represents an external person (client, supplier, staff, etc.)
    Can be linked to receipts, payments, debts, invoices, etc.
    """

    class PersonType(models.TextChoices):
        SUPPLIER = "supplier", _("Supplier")
        CLIENT = "client", _("Client")
        STAFF = "staff", _("Staff")
        OTHER = "other", _("Other")

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    type = models.CharField(max_length=20, choices=PersonType.choices, default=PersonType.OTHER, verbose_name=_("Type"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
