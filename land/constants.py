from django.utils.translation import gettext_lazy as _
from django.db import models

class LandType(models.TextChoices):
    AGRICULTURAL = "agricultural", _("Agricultural")
    RESIDENTIAL = "residential", _("Residential")
    COMMERCIAL = "commercial", _("Commercial")
    INDUSTRIAL = "industrial", _("Industrial")

class LandStatus(models.TextChoices):
    AVAILABLE = "available", _("Available")
    RENTED = "rented", _("Rented")
    UNDER_CULTIVATION = "cultivation", _("Under Cultivation")
    SOLD = "sold", _("Sold")
    OTHER = "other", _("Other")
