# farm_settings/admin.py
from django.contrib import admin
from farm_settings.models import FarmSettings
from farm_settings.models import Currency
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