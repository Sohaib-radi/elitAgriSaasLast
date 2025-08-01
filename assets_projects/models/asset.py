from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
import uuid
from core.models.base import FarmLinkedModel

class Asset(FarmLinkedModel):
    """Represents a physical or logical asset in the system.
    
    Assets can be agricultural, animal-related, or other types.
    Each asset has a purchase date, price, and expected lifespan.
    """
    class AssetType(models.TextChoices):
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
    
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    purchase_date = models.DateField(verbose_name=_('Purchase/Creation Date'))
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Price')
    )
    asset_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Asset Number")
    )

    asset_code = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        editable=False,
        verbose_name=_("Asset Code")
    )
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        verbose_name=_('Usage Type')
    )
    lifespan = models.PositiveIntegerField(
        help_text=_('Expected lifespan in days'),
        verbose_name=_('Lifespan')
    )
    primary_project = models.ForeignKey(
        'assets_projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_assets',
        verbose_name=_('Primary Project'),
        help_text=_("Main project this asset is linked to, if any.")
    )

    shared_projects = models.ManyToManyField(
        'assets_projects.Project',
        blank=True,
        related_name='shared_assets',
        verbose_name=_('Shared Projects'),
        help_text=_("Other projects this asset is used in.")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    supplier = models.ForeignKey(
        'product_catalogue.Supplier', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Supplier/Person ID')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.asset_code:
            self.asset_code = f"AS-PRJ-{uuid.uuid4().hex[:8].upper()}"
        if not self.asset_number:
            last = Asset.objects.filter(farm=self.farm).order_by("-id").first()
            next_number = (int(last.asset_number) + 1) if last and last.asset_number and last.asset_number.isdigit() else 1
            self.asset_number = f"{next_number:04d}"  # e.g., "0001", "0002"
        super().save(*args, **kwargs) 
    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"