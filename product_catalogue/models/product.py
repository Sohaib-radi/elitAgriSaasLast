# app: product_catalog/models/product.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.farm import Farm
from core.models.base import FarmLinkedModel
# --- CATEGORY AS TABLE ---
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        ordering = ['name']

    def __str__(self):
        return self.name

# --- PRODUCT MODEL ---
class Product(FarmLinkedModel):
    PRODUCT_TYPE_CHOICES = [
        ("animal", _("Animal")),
        ("agricultural", _("Agricultural")),
        ("other", _("Other")),
    ]
    name = models.CharField(max_length=255, verbose_name=_("Product Name"))
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Product Code"))
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_("Category")
    )
    type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, verbose_name=_("Type"))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price"))
    
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Weight (kg)")
    )
    description = models.TextField(blank=True, verbose_name=_("Description"))
    benefit = models.TextField(blank=True, verbose_name=_("Benefit"))
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Usage duration in days"),
        verbose_name=_("Usage Duration")
    )
    product_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Product shelf age in days"),
        verbose_name=_("Product Age")
    )
    storage_instructions = models.TextField(
        blank=True,
        verbose_name=_("Storage Instructions")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    """ farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Farm")
    ) """
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.category.name})"

# --- PRODUCT IMAGES ---
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Product")
    )
    image = models.ImageField(upload_to='product_images/', verbose_name=_("Image"))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name=_("Base Product")
    )
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Variant Code"))
    name = models.CharField(max_length=255, verbose_name=_("Variant Name"))
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Weight (kg)"))
    packaging = models.CharField(max_length=255, blank=True, verbose_name=_("Packaging Info"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.product.name})"
