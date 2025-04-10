from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import FarmLinkedModel
from core.models.person import Person

class Debt(FarmLinkedModel):
    """
    💰 Represents a financial debt related to a person (client, supplier, staff).
    Tracks repayment status, reason, and due date.
    """

    class DebtStatus(models.TextChoices):
        PENDING = 'pending', _("Due")
        PARTIALLY_PAID = 'partially_paid', _("Partially Paid")
        PAID = 'paid', _("Fully Paid")

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="debts",
        verbose_name=_("Person"),
        help_text=_("Person this debt is linked to."),
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Amount"))
    reason = models.CharField(max_length=255, verbose_name=_("Reason"))
    due_date = models.DateField(verbose_name=_("Due Date"))
    status = models.CharField(max_length=20, choices=DebtStatus.choices, default=DebtStatus.PENDING, verbose_name=_("Status"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Debt")
        verbose_name_plural = _("Debts")
        ordering = ["-due_date"]

    def __str__(self):
        return f"{self.person.name} - {self.amount} ({self.get_status_display()})"



class DebtAttachment(models.Model):
    """
    📎 Attachment linked to a specific debt (PDF, image, contract, etc.)
    """
    debt = models.ForeignKey(
        Debt,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Debt")
    )
    file = models.FileField(
        upload_to="debts/attachments/",
        verbose_name=_("Attachment File"),
        help_text=_("PDF, image, or document related to the debt.")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Debt Attachment")
        verbose_name_plural = _("Debt Attachments")

    def __str__(self):
        return f"{self.file.name}"