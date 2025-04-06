from django.db import models
from ..models.base import BaseModel
from django.utils.translation import gettext_lazy as _
from core.models.permissions import Permission 

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles', verbose_name=_("Permissions"))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name