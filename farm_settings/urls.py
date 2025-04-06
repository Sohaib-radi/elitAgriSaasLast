from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Farm settings views
from farm_settings.views.admin_currency import CurrencyAdminViewSet
from farm_settings.views.farm_settings import (
    MyFarmSettingsView,
    FarmSettingsAdminViewSet,
    FarmSettingsListView,
)

# Currency views
from farm_settings.views.currency import (
    AvailableCurrencyListView,
    FarmCurrencyViewSet,
    CurrencyRateView,
    CurrencyRateByDateView,
    CurrencyRateRangeView,
)

# Register routers
router = DefaultRouter()
router.register("admin", FarmSettingsAdminViewSet, basename="farm-settings-admin")
router.register("currencies", FarmCurrencyViewSet, basename="farm-currencies")
router.register("admin/currencies", CurrencyAdminViewSet, basename="admin-currency")
# Combine all urlpatterns
urlpatterns = [
    # Farm settings
    path("my/", MyFarmSettingsView.as_view(), name="my_farm_settings"),
    path("admin/<int:farm_id>/", FarmSettingsListView.as_view(), name="admin_farm_settings_by_farm"),

    # Currency
    path("currencies/available/", AvailableCurrencyListView.as_view(), name="available-currencies"),
    path("currencies/<int:pk>/rates/", CurrencyRateView.as_view(), name="currency-rates"),
    path("currencies/<int:pk>/rate-on-date/", CurrencyRateByDateView.as_view(), name="rate-on-date"),
    path("currencies/<int:pk>/rate-history/", CurrencyRateRangeView.as_view(), name="rate-history"),
    
    # Routers
    path("", include(router.urls)),
]
