from django.contrib import admin
from crop.models.crop import Crop
from crop.models.agricultural_land import AgriculturalLand
from crop.models.land_status import LandStatus


@admin.register(AgriculturalLand)
class AgriculturalLandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "land", "farm")
    search_fields = ("name", "code")
    list_filter = ("farm",)
    autocomplete_fields = ("land", "farm")


@admin.register(LandStatus)
class LandStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id", "agricultural_land", "status", "product_used", "quantity_used", "date", "farm"
    )
    list_filter = ("status", "date", "farm")
    search_fields = ("description",)
    autocomplete_fields = ("agricultural_land", "product_used", "farm")


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = (
        "id", "crop_type", "status", "quantity", "unit", "usage", "agricultural_land", "date", "farm"
    )
    list_filter = ("status", "usage", "date", "farm")
    search_fields = ("crop_type", "description")
    autocomplete_fields = ("agricultural_land", "farm")
