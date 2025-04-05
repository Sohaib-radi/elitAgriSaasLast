from django.contrib import admin
from product_catalogue.models import Product, ProductCategory, ProductImage, ProductVariant

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category']
    search_fields = ['name', 'code']
    list_filter = ['category']
    inlines = [ProductImageInline]

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'product', 'weight']
    search_fields = ['name', 'code']
    list_filter = ['product']