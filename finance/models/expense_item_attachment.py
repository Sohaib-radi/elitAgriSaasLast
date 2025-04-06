from django.db import models
from django.utils.translation import gettext_lazy as _
from finance.models.expense_item import ExpenseItem


class ExpenseItemAttachment(models.Model):
    """
     Attachment linked to an ExpenseItem (PDF, image, etc.)
    """
    expense_item = models.ForeignKey(
        ExpenseItem,
        on_delete=models.CASCADE,
        related_name="attachments",  # 🔗 this is the reverse link
        verbose_name=_("Expense Item"),
    )
    file = models.FileField(
        upload_to="expenses/attachments/",
        verbose_name=_("Attachment File"),
        help_text=_("PDF, image, or document related to the expense.")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Expense Attachment")
        verbose_name_plural = _("Expense Attachments")

    def __str__(self):
        return self.file.name
