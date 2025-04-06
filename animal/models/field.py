from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin


class FieldType(models.TextChoices):
    TEXT = "text", _("Text")
    NUMBER = "number", _("Number")
    DATE = "date", _("Date")
    BOOLEAN = "boolean", _("Yes/No")
    CHOICE = "choice", _("Single Choice")
    MULTI_CHOICE = "multi_choice", _("Multiple Choice")


class CustomListField(TimeStampedModel, CreatedByMixin):
    list = models.ForeignKey(
        "animal.AnimalList",
        on_delete=models.CASCADE,
        related_name="custom_fields",
        verbose_name=_("Animal List"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Field Name"))
    field_type = models.CharField(
        max_length=20,
        choices=FieldType.choices,
        default=FieldType.TEXT,
        verbose_name=_("Field Type"),
    )
    required = models.BooleanField(default=False, verbose_name=_("Required"))
    options = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Options"),
        help_text=_("Only used for choice/multi_choice fields"),
    )

    class Meta:
        verbose_name = _("Custom Field")
        verbose_name_plural = _("Custom Fields")

    def __str__(self):
        return f"{self.name} ({self.field_type})"
