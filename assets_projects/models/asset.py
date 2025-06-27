from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from core.models.base import FarmLinkedModel

class Asset(FarmLinkedModel):
    """Represents a physical or logical asset in the system.
    
    Assets can be agricultural, animal-related, or other types.
    Each asset has a purchase date, price, and expected lifespan.
    """
    class AssetType(models.TextChoices):
        AGRICULTURAL = 'agricultural', _('Agricultural')
        ANIMAL = 'animal', _('Animal')
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
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        verbose_name=_('Usage Type')
    )
    lifespan = models.PositiveIntegerField(
        help_text=_('Expected lifespan in days'),
        verbose_name=_('Lifespan')
    )
    project = models.ForeignKey(
        'assets_projects.Project',
        on_delete=models.CASCADE,
        related_name='assets',
        null=True,
        blank=True,
        verbose_name=_('Project')
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

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"