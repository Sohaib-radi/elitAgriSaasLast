from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        abstract = True
        ordering = ['-created_at']

class FarmLinkedModel(models.Model):
    farm = models.ForeignKey(
        "core.Farm",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        verbose_name=_("Farm")
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedByMixin(models.Model):
    created_by = models.ForeignKey(
        "core.User", 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name=_("Created By"),
        help_text=_("User who created this record."),
    )

    class Meta:
        abstract = True