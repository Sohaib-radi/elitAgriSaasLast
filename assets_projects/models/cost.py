from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from assets_projects.models.project import Project
from core.models.base import FarmLinkedModel
import uuid

class CostType(models.TextChoices):
        AGRICULTURAL = 'agricultural', _('Agricultural')
        ANIMAL = 'animal', _('Animal')
        CONSTRUCTION = 'construction', _('Construction')
        WAREHOUSE = 'warehouse', _('Warehouse')
        IRRIGATION = 'irrigation', _('Irrigation')
        GREENHOUSE = 'greenhouse', _('Greenhouse')
        AGRICULTURE = 'agriculture', _('Agriculture')
        LAND_DEVELOPMENT = 'land_development', _('Land Development')
        SOIL_IMPROVEMENT = 'soil_improvement', _('Soil Improvement')
        ANIMAL_HUSBANDRY = 'animal_husbandry', _('Animal Husbandry')
        VETERINARY = 'veterinary', _('Veterinary')
        BARN_CONSTRUCTION = 'barn_construction', _('Barn Construction')
        EQUIPMENT_PURCHASE = 'equipment_purchase', _('Equipment Purchase')
        TRANSPORTATION = 'transportation', _('Transportation')
        ELECTRICITY = 'electricity', _('Electricity')
        TRANSPORT = 'transport', _('Transport')
        MAINTENANCE = 'maintenance', _('Maintenance')
        PROCESSING = 'processing', _('Processing')
        RESEARCH = 'research', _('Research')
        TOOLS = 'tools', _('Tools')
        ADMINISTRATION = 'administration', _('Administration')
        OTHER = 'other', _('Other')

class ProjectCost(FarmLinkedModel):

    id = models.AutoField(primary_key=True, verbose_name=_('Number'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='costs',
        verbose_name=_('Project')
    )
    asset = models.ForeignKey(
        'Asset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Asset')
    )
    cost_type = models.CharField(
        max_length=20,
        choices=CostType.choices,
        default='other',
        verbose_name=_('Cost Type')
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Ammount')
    )
    cost_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Cost Number")
    )

    cost_code = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        editable=False,
        verbose_name=_("Cost Code")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Project Cost')
        verbose_name_plural = _('Projects Cost')
        ordering = ['-created_at']
    def save(self, *args, **kwargs):
        if not self.cost_code:
            self.cost_code = f"CT-PRJ-{uuid.uuid4().hex[:8].upper()}"
        if not self.cost_number:
            last = ProjectCost.objects.filter(farm=self.farm).order_by("-id").first()
            next_number = (int(last.cost_number) + 1) if last and last.cost_number and last.cost_number.isdigit() else 1
            self.cost_number = f"{next_number:04d}"  # e.g., "0001", "0002"
        super().save(*args, **kwargs) 
    def __str__(self):
        return f"{self.name} - {self.project.name}"