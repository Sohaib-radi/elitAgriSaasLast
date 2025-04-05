from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin

from core.models.base import FarmLinkedModel

class AnimalSpecies(models.TextChoices):
    COW = "cow", _("Cow")
    SHEEP = "sheep", _("Sheep")
    GOAT = "goat", _("Goat")
    CAMEL = "camel", _("Camel")
    CHICKEN = "chicken", _("Chicken")
    OTHER = "other", _("Other")


class AnimalGender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class AnimalStatus(models.TextChoices):
    PREGNANT = "pregnant", _("Pregnant")
    WITH_BABY = "with_baby", _("With Baby")
    NOT_PREGNANT = "not_pregnant", _("Not Pregnant")
    HEALTHY = "healthy", _("Healthy")
    SICK = "sick", _("Sick")
    DECEASED = "deceased", _("Deceased")


class Animal(TimeStampedModel, CreatedByMixin,FarmLinkedModel):
    """ farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="animals",
        verbose_name=_("Farm"),
        help_text=_("The farm this animal belongs to."),
    ) """

    list = models.ForeignKey(
        "animal.AnimalList",
        on_delete=models.CASCADE,
        related_name="animals",
        verbose_name=_("Animal List"),
        help_text=_("The custom list/category the animal is part of."),
    )

    animal_number = models.CharField(
        max_length=100,
        verbose_name=_("Animal Number"),
        help_text=_("Farm-specific identifier for the animal."),
        db_index=True,
    )

    international_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("International Number"),
        help_text=_("Official registration number (e.g., RFID tag)."),
        db_index=True,
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Name"),
        help_text=_("Optional nickname for the animal."),
    )

    species = models.CharField(
        max_length=20,
        choices=AnimalSpecies.choices,
        default=AnimalSpecies.OTHER,
        verbose_name=_("Species"),
        help_text=_("The species of the animal (cow, sheep, etc.)."),
    )

    breed = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Breed"),
        help_text=_("Breed of the animal."),
    )

    gender = models.CharField(
        max_length=10,
        choices=AnimalGender.choices,
        verbose_name=_("Gender"),
        help_text=_("Gender of the animal."),
    )

    birth_date = models.DateField(
        verbose_name=_("Birth Date"),
        help_text=_("Date of birth."),
    )

    status = models.CharField(
        max_length=20,
        choices=AnimalStatus.choices,
        default=AnimalStatus.HEALTHY,
        verbose_name=_("Status"),
        help_text=_("Current health or reproductive status."),
    )

    mother = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mothered_animals",
        verbose_name=_("Mother"),
        help_text=_("Reference to the mother animal."),
    )

    father = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fathered_animals",
        verbose_name=_("Father"),
        help_text=_("Reference to the father animal."),
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Additional notes or remarks."),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Soft-delete flag for animal records."),
    )

    class Meta:
        verbose_name = _("Animal")
        verbose_name_plural = _("Animals")
        ordering = ["-created_at"]
        unique_together = ("farm", "animal_number")

    def __str__(self):
        return f"{self.animal_number} - {self.species}"
