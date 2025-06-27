from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.base import FarmLinkedModel

class Project(FarmLinkedModel):
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    parent_project = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Parent Project')
    )
    description = models.TextField(verbose_name=_('Description'))
    address = models.TextField(verbose_name=_('Address'))
    image = models.ImageField(
        upload_to='projects/',
        null=True,
        blank=True,
        verbose_name=_('Image')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def __str__(self):
        return self.name