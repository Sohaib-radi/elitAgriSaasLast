from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin

from animal.models.animal import Animal
from core.models.base import FarmLinkedModel

class BirthStatus(models.TextChoices):
    HEALTHY = "healthy", _("Healthy")                                       #  Normal birth
    WEAK = "weak", _("Weak")                                                #  Alive but fragile
    STILLBORN = "stillborn", _("Stillborn")                                 #  Dead on delivery
    DIED_AFTER_BIRTH = "died_after_birth", _("Died Shortly After Birth")    #  Died within days
    ABORTED = "aborted", _("Aborted")                                       #  Forced abortion or miscarriage
    UNKNOWN = "unknown", _("Unknown")                                       # ❔ Not specified


class AnimalBirth(TimeStampedModel,FarmLinkedModel, CreatedByMixin):
    """ farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="animal_births",
        verbose_name=_("Farm"),
        help_text=_("The farm this birth record belongs to.")
    ) """

    list = models.ForeignKey(
        "animal.AnimalList",
        on_delete=models.CASCADE,
        related_name="births",
        verbose_name=_("Animal List"),
        help_text=_("The list the animal will be moved to after birth.")
    )

    mother = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="births_as_mother",
        verbose_name=_("Mother"),
        help_text=_("The mother animal.")
    )

    father = models.ForeignKey(
        Animal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="births_as_father",
        verbose_name=_("Father"),
        help_text=_("The father animal (optional).")
    )

    animal_number = models.CharField(
        max_length=100,
        verbose_name=_("Animal Number"),
        help_text=_("Farm-specific identifier for the newborn."),
        db_index=True
    )

    international_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("International Number"),
        help_text=_("Official registration number (e.g. RFID tag)."),
        db_index=True
    )

    species = models.CharField(
        max_length=20,
        verbose_name=_("Species"),
        help_text=_("Species of the newborn (cow, sheep, etc.).")
    )

    gender = models.CharField(
        max_length=10,
        verbose_name=_("Gender"),
        help_text=_("Gender of the newborn.")
    )

    birth_datetime = models.DateTimeField(
        verbose_name=_("Birth Date and Time"),
        help_text=_("Exact date and time of birth.")
    )

    status = models.CharField(
        max_length=30,
        choices=BirthStatus.choices,
        default=BirthStatus.HEALTHY,
        verbose_name=_("Birth Status"),
        help_text=_("Status of the newborn at birth.")
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Any notes or observations about the birth.")
    )

    moved_to_animals = models.BooleanField(
        default=False,
        verbose_name=_("Moved to Animals"),
        help_text=_("Has the newborn been transferred to the main animal list?")
    )

    class Meta:
        verbose_name = _("Animal Birth")
        verbose_name_plural = _("Animal Births")
        ordering = ["-birth_datetime"]

    def __str__(self):
        return f"Birth #{self.animal_number} ({self.species})"
