# farm_settings/admin.py
from django.contrib import admin
from farm_settings.models import FarmSettings
from farm_settings.models import Currency
from farm_settings.models.farm_settings import DefaultFarmImage
@admin.register(FarmSettings)
class FarmSettingsAdmin(admin.ModelAdmin):
    list_display = ["farm", "default_language", "currency", "multi_farm_enabled", "created_at"]
    search_fields = ["farm__name", "legal_name", "contact_person", "email"]
    list_filter = ["default_language", "multi_farm_enabled", "ai_enabled"]
    autocomplete_fields = ["farm"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    search_fields = ["code", "name"]


@admin.register(DefaultFarmImage)
class DefaultFarmImageAdmin(admin.ModelAdmin):
    list_display = ("farm", "type", "image_preview")
    list_filter = ("farm", "type")
    search_fields = ("farm__name",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit:contain;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"