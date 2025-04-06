from django.db import models
from django.utils.translation import gettext_lazy as _
from finance.models.receipt import Receipt


class ReceiptAttachment(models.Model):
    """
    📎 Attachment linked to a receipt (PDF, image, document)
    """
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Receipt"),
    )
    file = models.FileField(
        upload_to="receipts/attachments/",
        verbose_name=_("Attachment File"),
        help_text=_("PDF, image, or document related to the receipt.")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Receipt Attachment")
        verbose_name_plural = _("Receipt Attachments")

    def __str__(self):
        return self.file.name
