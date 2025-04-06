from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class EntryPresence(models.TextChoices):
    REAL = "real", _("Real (Physical)")
    VIRTUAL = "virtual", _("Virtual (Logical)")

class WarehouseEntry(models.Model):
    
    def default_today():
        return timezone.now().date()
    
    warehouse = models.ForeignKey(
        "warehouse.Warehouse",
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name=_("Warehouse")
    )
    #The Id of Model Entry ex: Animal Model ->  ID = 6
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Entry Type")
    )
    #The Id of object exemple: Animal width Id -> 1
    object_id = models.PositiveIntegerField(verbose_name=_("Reference ID"))
    content_object = GenericForeignKey("content_type", "object_id")
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity"))
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Weight"))
    space_taken = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Space Taken (m²)"))
    date_added = models.DateField(default=default_today, verbose_name=_("Date Added"))

    
    entry_presence = models.CharField(
        max_length=10,
        choices=EntryPresence.choices,
        default=EntryPresence.REAL,
        verbose_name=_("Entry Presence Type")
    )

    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    class Meta:
        verbose_name = _("Warehouse Entry")
        verbose_name_plural = _("Warehouse Entries")
        ordering = ["-date_added"]
