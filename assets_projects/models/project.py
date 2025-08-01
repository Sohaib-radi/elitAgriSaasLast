from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from core.models.base import FarmLinkedModel
from core.models import Attachment  
from django.contrib.contenttypes.models import ContentType
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Project(FarmLinkedModel):
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    project_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Project Number")
    )

    project_code = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        editable=False,
        verbose_name=_("Project Code")
    )

    parent_project = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Parent Project')
    )

    description = models.TextField(verbose_name=_('Description'))
    address = models.TextField(verbose_name=_('Address'))

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Start Date"),
        help_text=_("Date when the project is planned to start")
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("End Date"),
        help_text=_("Date when the project is planned to end")
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Is Active"),
        help_text=_("Mark whether the project is currently active or not.")
    )

    total_costs = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        editable=False,
        verbose_name=_("Total Costs")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.project_code:
            self.project_code = f"PRJ-{uuid.uuid4().hex[:8].upper()}"
        if not self.project_number:
            last = Project.objects.filter(farm=self.farm).order_by("-id").first()
            next_number = (
                int(last.project_number) + 1
                if last and last.project_number and last.project_number.isdigit()
                else 1
            )
            self.project_number = f"{next_number:04d}"  # e.g., "0001", "0002"
        super().save(*args, **kwargs)

    def update_total_costs(self):
        """
        Aggregate and store total costs from related cost items.
        Called manually or via signals.
        """
        total = self.costs.aggregate(total=Sum('amount'))['total'] or 0
        self.total_costs = total
        self.save(update_fields=['total_costs'])

    @property
    def primary_image(self):
        return self.get_primary_image()

    def get_attachments(self):
        """
        Get all attachments related to this project.
        """
        content_type = ContentType.objects.get_for_model(self)
        return Attachment.objects.filter(content_type=content_type, object_id=self.id)

    def get_images(self):
        """
        Get only image attachments.
        """
        return self.get_attachments().filter(file_type='image')

    def get_primary_image(self):
        """
        Get the first image attachment (could be considered the primary image).
        """
        return self.get_images().first()