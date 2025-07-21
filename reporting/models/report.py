# reporting/models/report.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ReportRecord(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        SUCCESS = "success", _("Success")
        FAILED = "failed", _("Failed")

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)  # e.g. 'animal_death'
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    filters = models.JSONField(null=True, blank=True)
    file_path = models.FileField(upload_to="reports/", null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Report Record")
        verbose_name_plural = _("Report Records")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.status}"
