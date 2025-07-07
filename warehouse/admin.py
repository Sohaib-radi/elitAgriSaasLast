from django.contrib import admin

from warehouse.models.entry import WarehouseEntry
from warehouse.models.warehouse import Warehouse, WarehouseImage, WarehouseVideo

# Register your models here.
@admin.register(WarehouseEntry)
class WarehouseEntryAdmin(admin.ModelAdmin):
    list_display = ["warehouse", "reference_name", "model_type", "quantity", "entry_presence", "date_added"]
    list_filter = ["entry_presence", "content_type"]
    search_fields = ["object_id"]




# Inline for WarehouseImage
class WarehouseImageInline(admin.TabularInline):
    model = WarehouseImage
    extra = 0
    fields = [
        f.name for f in WarehouseImage._meta.fields
        if f.editable and f.name != "id"
    ]

# Inline for WarehouseVideo
class WarehouseVideoInline(admin.TabularInline):
    model = WarehouseVideo
    extra = 0
    fields = [
        f.name for f in WarehouseVideo._meta.fields
        if f.editable and f.name != "id"
    ]

# Warehouse admin with inlines
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Warehouse._meta.fields]
    search_fields = ['name', 'location']
    inlines = [WarehouseImageInline, WarehouseVideoInline]
