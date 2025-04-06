from django.db import models
from django.utils.translation import gettext_lazy as _
from finance.models.payment import Payment


class PaymentAttachment(models.Model):
    """
    Attachment linked to a payment.
    """
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Payment"),
    )
    file = models.FileField(
        upload_to="payments/attachments/",
        verbose_name=_("Attachment File"),
        help_text=_("PDF, image, or document related to the payment.")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Payment Attachment")
        verbose_name_plural = _("Payment Attachments")

    def __str__(self):
        return self.file.name
