from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin

class AnimalCustomFieldValue(TimeStampedModel, CreatedByMixin):
    animal = models.ForeignKey("animal.Animal", on_delete=models.CASCADE, related_name="custom_field_values")
    field = models.ForeignKey("animal.CustomListField", on_delete=models.CASCADE)
    value = models.TextField(verbose_name=_("Value"))

    class Meta:
        unique_together = ("animal", "field")
        verbose_name = _("Animal Custom Field Value")
        verbose_name_plural = _("Animal Custom Field Values")

    def __str__(self):
        return f"{self.animal.animal_number} - {self.field.name}: {self.value}"
