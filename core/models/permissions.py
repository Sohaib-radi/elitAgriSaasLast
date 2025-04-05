from django.db import models
from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    """
    Represents a system-wide action like 'animals.view' or 'reports.export'
    """
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Code"))
    label = models.CharField(max_length=255, verbose_name=_("Label"))
    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")

    def __str__(self):
        return self.label


