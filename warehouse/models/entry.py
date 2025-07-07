# warehouse/models/entry.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class EntryPresence(models.TextChoices):
    REAL = "real", _("Real (Physical)")
    VIRTUAL = "virtual", _("Virtual (Logical)")

class EntryStatus(models.TextChoices):
    IN_STOCK = "in_stock", _("In Stock")
    REMOVED = "removed", _("Removed")
    TRANSFERRED = "transferred", _("Transferred")

def default_today():
    return timezone.now().date()

class WarehouseEntry(models.Model):
    """
    Represents an entry in a warehouse, tracking products, animals, crops, etc.,
    with quantity, weight, space taken, status, and advanced audit tracking.
    """

    warehouse = models.ForeignKey(
        "warehouse.Warehouse",
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name=_("Warehouse")
    )

    # The ID of the model entry, e.g., Animal, Product, Crop
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Entry Type")
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Reference ID"))
    content_object = GenericForeignKey("content_type", "object_id")

    ORIGIN_CHOICES = [
        ("produced", _("Produced by farm")),
        ("purchased", _("Purchased externally")),
    ]
    origin = models.CharField(
        max_length=20,
        choices=ORIGIN_CHOICES,
        default="purchased",
        verbose_name=_("Origin")
    )

    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity"))
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Weight"))
    space_taken = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Space Taken (m²)"))

    entry_presence = models.CharField(
        max_length=10,
        choices=EntryPresence.choices,
        default=EntryPresence.REAL,
        verbose_name=_("Entry Presence Type")
    )

    status = models.CharField(
        max_length=20,
        choices=EntryStatus.choices,
        default=EntryStatus.IN_STOCK,
        verbose_name=_("Status")
    )

    barcode = models.CharField(max_length=255, blank=True, verbose_name=_("Barcode"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    date_added = models.DateField(default=default_today, verbose_name=_("Date Added"))

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def reference_name(self):
        return str(self.content_object) if self.content_object else "—"

    def is_product_entry(self):
        return self.content_type.model == "product"

    @property
    def model_type(self):
        return self.content_type.model

    class Meta:
        verbose_name = _("Warehouse Entry")
        verbose_name_plural = _("Warehouse Entries")
        ordering = ["-date_added"]
        indexes = [
            models.Index(fields=["warehouse", "content_type", "object_id"]),
            models.Index(fields=["date_added"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.reference_name()} - {self.quantity}"

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete for archival instead of permanent removal.
        """
        self.is_active = False
        self.save()
