from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from assets_projects.models.project import Project
from core.models.base import FarmLinkedModel

class ProjectCost(FarmLinkedModel):
    id = models.AutoField(primary_key=True, verbose_name=_('Number'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='costs',
        verbose_name=_('Project')
    )
    asset = models.ForeignKey(
        'Asset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Asset')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Ammount')
    )
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Project Cost')
        verbose_name_plural = _('Projects Cost')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.project.name}"