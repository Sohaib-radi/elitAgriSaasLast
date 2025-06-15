from django.db import models
from django.utils.translation import gettext_lazy as _
from product_catalogue.models.supplier import Supplier

class SupplierAttachment(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Supplier")
    )
    file = models.FileField(
        upload_to='supplier_attachments/',
        verbose_name=_("File")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("File Name")
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Uploaded At")
    )

    class Meta:
        verbose_name = _("Supplier Attachment")
        verbose_name_plural = _("Supplier Attachments")
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.name
