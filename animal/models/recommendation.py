from django.db import models
from django.utils.translation import gettext_lazy as _
from animal.models.animal import AnimalSpecies


class VaccineRecommendation(models.Model):
    species = models.CharField(
        max_length=50,
        choices=AnimalSpecies.choices,
        verbose_name=_("Species"),
        help_text=_("Animal species this recommendation applies to."),
    )

    vaccine_name = models.CharField(
        max_length=150,
        verbose_name=_("Vaccine Name"),
        help_text=_("Scientific or commercial name of the vaccine."),
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Explanation of why and when the vaccine is recommended."),
    )

    recommended_age_days = models.PositiveIntegerField(
        verbose_name=_("Recommended Age (Days)"),
        help_text=_("Age in days when the vaccine should be administered."),
    )

    repeat_interval_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Repeat Interval (Days)"),
        help_text=_("How often the vaccine should be repeated (if applicable)."),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Vaccine Recommendation")
        verbose_name_plural = _("Vaccine Recommendations")
        unique_together = ("species", "vaccine_name", "recommended_age_days")

    def __str__(self):
        return f"{self.species} - {self.vaccine_name} at {self.recommended_age_days}d"
