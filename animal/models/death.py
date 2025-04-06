from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin
from animal.models.animal import Animal
from core.models.base import FarmLinkedModel

class AnimalDeathStatus(models.TextChoices):
    PENDING_REVIEW = "pending", _("Pending Review")
    CONFIRMED = "confirmed", _("Confirmed")
    REJECTED = "rejected", _("Rejected")
    ARCHIVED = "archived", _("Archived")


class AnimalDeath( TimeStampedModel, CreatedByMixin, FarmLinkedModel):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="deaths",
        verbose_name=_("Animal"),
        help_text=_("Animal that has died."),
    )
    """ farm = models.ForeignKey(
        'core.Farm',
        on_delete=models.CASCADE,
        verbose_name=_("Farm"),
        help_text=_("The farm this death record belongs to."),
    ) """
    death_datetime = models.DateTimeField(
        verbose_name=_("Date and Time"),
        help_text=_("Date and time of death."),
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Reason"),
        help_text=_("Optional cause of death."),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Any additional notes."),
    )
    status = models.CharField(
        max_length=20,
        choices=AnimalDeathStatus.choices,
        default=AnimalDeathStatus.PENDING_REVIEW,
        verbose_name=_("Status"),
        help_text=_("Status of this death record."),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Animal Death")
        verbose_name_plural = _("Animal Deaths")
        ordering = ["-death_datetime"]

    def __str__(self):
        return f"Death of {self.animal}"


class AnimalDeathImage(models.Model):
    death = models.ForeignKey(
        AnimalDeath,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Death Record"),
    )
    image = models.ImageField(upload_to="animal/deaths/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Death Image")
        verbose_name_plural = _("Death Images")

    def __str__(self):
        return f"Image for death ID {self.death_id}"
