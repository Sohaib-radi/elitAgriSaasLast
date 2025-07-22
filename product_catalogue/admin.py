from typing import __all__
from django.contrib import admin
from product_catalogue.models import Product, ProductCategory, ProductImage, ProductVariant
from product_catalogue.models.personal_product import PersonalProduct
from product_catalogue.models.project import Project
from product_catalogue.models.supplier import Supplier



def all_fields(model):
    return [field.name for field in model._meta.fields]

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

@admin.register(PersonalProduct)
class PersonalProductAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'notes', 'project', 'product']
    search_fields = ['product']
    list_filter = ['quantity','product']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date','is_active']
    search_fields = ['name', 'is_active']
    list_filter = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
     list_display = all_fields(Supplier)