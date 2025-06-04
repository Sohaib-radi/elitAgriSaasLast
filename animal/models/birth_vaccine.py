from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin
from animal.models.birth import AnimalBirth
from animal.models.vaccine import VaccineStatus


class AnimalBirthVaccine(TimeStampedModel, CreatedByMixin):
    birth = models.ForeignKey(
        AnimalBirth,
        on_delete=models.CASCADE,
        related_name="planned_vaccines",
        verbose_name=_("Animal Birth"),
        help_text=_("Birth entry this vaccine is linked to."),
    )

    name = models.CharField(
        max_length=200,
        verbose_name=_("Vaccine Name"),
        help_text=_("Name of the recommended vaccine."),
    )

    date_given = models.DateField(
        verbose_name=_("Scheduled Date"),
        help_text=_("Date the vaccine is recommended to be given."),
    )

    valid_until = models.DateField(
        verbose_name=_("Valid Until"),
        help_text=_("How long the vaccine remains valid."),
    )

    status = models.CharField(
        max_length=20,
        choices=VaccineStatus.choices,
        default=VaccineStatus.SCHEDULED,
        verbose_name=_("Status"),
        help_text=_("Current status of the vaccine."),
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Optional notes."),
    )

    image = models.ImageField(
        upload_to="animal/birth_vaccines/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_("Optional image proof."),
    )

    class Meta:
        verbose_name = _("Planned Vaccine for Birth")
        verbose_name_plural = _("Planned Vaccines for Birth")
        unique_together = ("birth", "name", "date_given")

    def __str__(self):
        return f"{self.name} for {self.birth.animal_number} on {self.date_given}"
