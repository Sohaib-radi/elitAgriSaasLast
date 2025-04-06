from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import TimeStampedModel, CreatedByMixin
from core.models.farm import Farm
from core.models.base import FarmLinkedModel

class AnimalList( TimeStampedModel, CreatedByMixin,FarmLinkedModel):
    """
    A list/category of animals defined by the farm (e.g. Sheep, Cows).
    Animals and custom fields are linked to this list.
    """

    """ farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="animal_lists",
        verbose_name=_("Farm"),
        help_text=_("The farm this list belongs to."),
    ) """

    name = models.CharField(
        max_length=100,
        verbose_name=_("List Name"),
        help_text=_("Name of the list, e.g., Sheep, Cows."),
        db_index=True,
    )

    image = models.ImageField(
        upload_to="animal/list-images/",
        blank=True,
        null=True,
        verbose_name=_("List Image"),
        help_text=_("Optional image to visually identify the list."),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Soft delete flag for the list."),
    )

    class Meta:
        verbose_name = _("Animal List")
        verbose_name_plural = _("Animal Lists")
        unique_together = ("farm", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.farm.name})"
