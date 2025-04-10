from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel

class ServiceCompany(FarmLinkedModel):
    """
    🏢 Represents a service provider (e.g., electricity, water, gas).
    """
    SERVICE_CHOICES = [
        ('water', _("Water")),
        ('electricity', _("Electricity")),
        ('gas', _("Gas")),
        ('internet', _("Internet")),
        ('other', _("Other")),
    ]

    company_number = models.CharField(max_length=50, unique=True, verbose_name=_("Company Number"))
    name = models.CharField(max_length=255, verbose_name=_("Company Name"))
    branch_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Branch Name"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Branch Address"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, verbose_name=_("Service Type"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"
