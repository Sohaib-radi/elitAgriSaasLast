from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin
from animal.models.animal import Animal


class VaccineStatus(models.TextChoices):
    SCHEDULED = "scheduled", _("Scheduled")
    GIVEN = "given", _("Given")
    EXPIRED = "expired", _("Expired")
    VALID = "valid", _("Valid")


class AnimalVaccine(TimeStampedModel, CreatedByMixin, models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="vaccines",
        verbose_name=_("Animal"),
        help_text=_("The animal receiving the vaccine."),
    )

    name = models.CharField(
        max_length=200,
        verbose_name=_("Vaccine Name"),
        help_text=_("Name of the vaccine administered."),
    )

    date_given = models.DateField(
        verbose_name=_("Date Given"),
        help_text=_("Date the vaccine was administered."),
    )

    valid_until = models.DateField(
        verbose_name=_("Valid Until"),
        help_text=_("Expiry or validity date of the vaccine."),
    )

    status = models.CharField(
        max_length=20,
        choices=VaccineStatus.choices,
        default=VaccineStatus.GIVEN,
        verbose_name=_("Status"),
        help_text=_("Current status of the vaccination."),
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Optional notes or observations."),
    )

    image = models.ImageField(
        upload_to="animal/vaccines/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_("Optional image proof of vaccination."),
    )

    class Meta:
        verbose_name = _("Animal Vaccine")
        verbose_name_plural = _("Animal Vaccines")
        ordering = ["-date_given"]
        unique_together = ("animal", "name", "date_given")

    def __str__(self):
        return f"{self.name} - {self.animal.animal_number}"
