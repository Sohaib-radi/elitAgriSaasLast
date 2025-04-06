from django.contrib import admin
from land.models.land import Land
from land.models.wilaya import Wilaya
from land.models.purchase import LandPurchase
from land.models.media import LandDocument
from land.models.media import LandImage

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ("land_number", "international_number","latitude", "longitude", "google_maps_url", "wilaya", "land_type", "area", "status", "purchase_date")
    search_fields = ("land_number", "international_number", "address")
    list_filter = ("land_type", "status", "wilaya")

@admin.register(Wilaya)
class WilayaAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(LandPurchase)
class LandPurchaseAdmin(admin.ModelAdmin):
    list_display = ("land", "transaction_type", "purchase_price", "purchase_date", "buyer", "seller_name")

@admin.register(LandDocument)
class LandDocumentAdmin(admin.ModelAdmin):
    list_display = ("land", "document", "created_at")
    search_fields = ("land__land_number",)

@admin.register(LandImage)
class LandImageAdmin(admin.ModelAdmin):
    list_display = ("land", "image", "created_at")
    search_fields = ("land__land_number",)
