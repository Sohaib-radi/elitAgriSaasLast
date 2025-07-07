from django.db import models
from core.models.base import FarmLinkedModel
from django.utils.translation import gettext_lazy as _


class Warehouse(FarmLinkedModel):
    """
    Represents a physical or logical warehouse in the farm, including
    description, space, location, and media for advanced operational management.
    """

    name = models.CharField(max_length=255, verbose_name=_("Warehouse Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    space = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Space (m²)")
    )

    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Latitude")
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Longitude")
    )

    image = models.ImageField(
        upload_to="warehouses/images/",
        null=True,
        blank=True,
        verbose_name=_("Main Image")
    )

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    created_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    @property
    def google_maps_url(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete for archival instead of permanent removal.
        """
        self.is_active = False
        self.save()

class WarehouseImage(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="warehouses/gallery/", verbose_name=_("Image"))
    title = models.CharField(max_length=255, verbose_name=_("Image Title"))
    description = models.TextField(blank=True, verbose_name=_("Image Description"))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Warehouse Image")
        verbose_name_plural = _("Warehouse Images")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class WarehouseVideo(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="warehouses/videos/", verbose_name=_("Video"))
    title = models.CharField(max_length=255, verbose_name=_("Video Title"))
    description = models.TextField(blank=True, verbose_name=_("Video Description"))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Warehouse Video")
        verbose_name_plural = _("Warehouse Videos")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
