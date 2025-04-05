from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin


class AnimalImage(TimeStampedModel, CreatedByMixin,models.Model):
    animal = models.ForeignKey(
        "animal.Animal",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Animal"),
        help_text=_("The animal this image belongs to."),
    )

    image = models.ImageField(
        upload_to="animal/images/",
        verbose_name=_("Image"),
        help_text=_("Photo of the animal."),
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Caption"),
        help_text=_("Optional caption or description."),
    )

    class Meta:
        verbose_name = _("Animal Image")
        verbose_name_plural = _("Animal Images")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Image for {self.animal.animal_number}"
