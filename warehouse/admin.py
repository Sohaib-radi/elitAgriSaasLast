from django.contrib import admin

from warehouse.models.entry import WarehouseEntry

# Register your models here.
@admin.register(WarehouseEntry)
class WarehouseEntryAdmin(admin.ModelAdmin):
    list_display = ["warehouse", "reference_name", "model_type", "quantity", "entry_presence", "date_added"]
    list_filter = ["entry_presence", "content_type"]
    search_fields = ["object_id"]