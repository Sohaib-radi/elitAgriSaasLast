import uuid
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from core.models.farm import Farm
from land.constants import LandType, LandStatus
from land.models.wilaya import Wilaya
from django.contrib.auth import get_user_model
from core.models.base import TimeStampedModel, CreatedByMixin
from core.models.base import FarmLinkedModel
User = get_user_model()

class Land(CreatedByMixin,FarmLinkedModel):
    """
    Core model to store land information.
    """
    
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    international_number = models.CharField(max_length=100, unique=True, verbose_name=_("International Number"))
    land_number = models.CharField(max_length=100, db_index=True, verbose_name=_("Land Number"))
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name="lands", verbose_name=_("Wilaya"))
    address = models.TextField(verbose_name=_("Address"))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price (USD)"))
    purchase_date = models.DateTimeField(default=now, verbose_name=_("Purchase Date"))
    land_type = models.CharField(max_length=50, choices=LandType.choices, verbose_name=_("Land Type"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Area (sqm)"))
    circumference = models.CharField(max_length=50,  verbose_name=_("Earth's circumference"))

    status = models.CharField(max_length=20, choices=LandStatus.choices, default=LandStatus.AVAILABLE, verbose_name=_("Land Status"))
    

    current_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="owned_lands", verbose_name=_("Current Owner")
    )
    previous_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="previously_owned_lands", verbose_name=_("Previous Owner")
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        verbose_name=_("Latitude"),
        help_text=_("GPS latitude in decimal degrees.")
    )

    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True,
        verbose_name=_("Longitude"),
        help_text=_("GPS longitude in decimal degrees.")
    )

    google_maps_url = models.URLField(
        max_length=500,
        null=True, blank=True,
        verbose_name=_("Google Maps URL"),
        help_text=_("Direct URL to the land on Google Maps.")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    class Meta:
        verbose_name = _("Land")
        verbose_name_plural = _("Lands")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["international_number"]),
            models.Index(fields=["land_number"]),
            models.Index(fields=["wilaya"]),
        ]

    def __str__(self):
        return f"{self.land_number} - {self.wilaya.name}"
    
    def save(self, *args, **kwargs):
        if self.latitude and self.longitude and not self.google_maps_url:
            self.google_maps_url = f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        super().save(*args, **kwargs)

    def mark_as_sold(self, buyer):
        """
        Marks the land as sold and updates the owner.
        """
        self.previous_owner = self.current_owner
        self.current_owner = buyer
        self.status = LandStatus.SOLD
        self.save()
