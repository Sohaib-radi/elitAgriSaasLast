from django.db import models
from core.models.base import TimeStampedModel, CreatedByMixin
from land.models.land import Land
from django.utils.translation import gettext_lazy as _


class LandImage(TimeStampedModel, CreatedByMixin):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="images", verbose_name=_("Land"))
    image = models.ImageField(upload_to="land/images/", verbose_name=_("Image"))
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Caption"))

    def __str__(self):
        return f"Image for {self.land.land_number}"

class LandDocument(TimeStampedModel, CreatedByMixin):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="documents", verbose_name=_("Land"))
    document = models.FileField(upload_to="land/documents/", verbose_name=_("Document"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return f"{self.title} ({self.land.land_number})"