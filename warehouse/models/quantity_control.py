# warehouse/models/quantity_control.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models.base import FarmLinkedModel


class WarehouseQuantitySchedule(FarmLinkedModel):
    """
    Scheduled quantity changes for a warehouse item (e.g. auto-increase/decrease).
    """
    warehouse = models.ForeignKey("warehouse.Warehouse", on_delete=models.CASCADE, related_name="quantity_schedules")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reference = GenericForeignKey("content_type", "object_id")

    ACTION_CHOICES = [
        ("increase", _("Increase")),
        ("decrease", _("Decrease")),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name=_("Action"))
    frequency = models.CharField(max_length=50, verbose_name=_("Frequency (e.g. daily, weekly)"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"))

    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Warehouse Quantity Schedule")
        verbose_name_plural = _("Warehouse Quantity Schedules")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_action_display()} {self.amount} every {self.frequency}"


class WarehouseReminder(FarmLinkedModel):
    """
    Reminder when quantity drops below threshold for an item in a warehouse.
    """
    warehouse = models.ForeignKey("warehouse.Warehouse", on_delete=models.CASCADE, related_name="reminders")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reference = GenericForeignKey("content_type", "object_id")

    alert_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Alert Quantity"))

    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Warehouse Reminder")
        verbose_name_plural = _("Warehouse Reminders")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert if < {self.alert_quantity}"
