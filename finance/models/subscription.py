from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from finance.models.service_company import ServiceCompany

class Subscription(FarmLinkedModel):
    """
    🔁 Represents a recurring subscription (e.g., utility, internet, etc.)
    """
    subscription_number = models.CharField(max_length=50, unique=True, verbose_name=_("Subscription Number"))
    name = models.CharField(max_length=255, verbose_name=_("Subscription Name"))
    company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, related_name="subscriptions", verbose_name=_("Service Company"))
    account_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Account Number"))
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Monthly Amount"))
    payment_method = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Payment Method"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End Date"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    image = models.ImageField(upload_to="subscriptions/", blank=True, null=True, verbose_name=_("Attachment"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
