from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Attachment(BaseModel):
    """
    A generic attachment that can be linked to any model (BankTransaction, LoanPayment, Check, etc.).
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content Type"),
        help_text=_("Content type of the related object.")
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Object ID"),
        help_text=_("ID of the related object.")
    )
    content_object = GenericForeignKey("content_type", "object_id")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Attachment Name"),
        help_text=_("Readable name for this attachment (optional)."),
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to="attachments/%Y/%m/%d/",
        verbose_name=_("File"),
        help_text=_("The attached file.")
    )
    file_type = models.CharField(
        max_length=50,
        verbose_name=_("File Type"),
        help_text=_("Type of the file (image, pdf, etc.)."),
        blank=True,
        null=True
    )
    extension = models.CharField(
        max_length=10,
        verbose_name=_("File Extension"),
        help_text=_("File extension, e.g., pdf, jpg."),
        blank=True,
        null=True
    )
    size = models.PositiveBigIntegerField(
        verbose_name=_("File Size (bytes)"),
        help_text=_("Size of the file in bytes."),
        blank=True,
        null=True
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_("Uploaded By"),
        help_text=_("User who uploaded this attachment."),
        null=True,
        blank=True,
        related_name="uploaded_attachments"
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        help_text=_("Optional description for this attachment."),
        blank=True,
        null=True
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name=_("Is Public"),
        help_text=_("Whether this attachment is publicly accessible.")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Timestamp when this attachment was created.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Timestamp when this attachment was last updated.")
    )

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Auto-extract extension and size
        if self.file:
            name, extension = os.path.splitext(self.file.name)
            self.extension = extension.lower().replace(".", "")
            self.size = self.file.size
            if not self.file_type:
                if self.extension in ["jpg", "jpeg", "png", "gif"]:
                    self.file_type = "image"
                elif self.extension == "pdf":
                    self.file_type = "pdf"
                elif self.extension in ["doc", "docx"]:
                    self.file_type = "word"
                elif self.extension in ["xls", "xlsx"]:
                    self.file_type = "excel"
                else:
                    self.file_type = "other"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or os.path.basename(self.file.name)
