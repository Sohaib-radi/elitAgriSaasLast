

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from crop.views.agricultural_land import AgriculturalLandViewSet
from crop.views.land_status import LandStatusViewSet
from crop.views.crop import CropViewSet
from crop.views.statistics import CropStatisticsView

router = DefaultRouter()
router.register("agricultural-lands", AgriculturalLandViewSet, basename="agricultural-land")
router.register("land-status", LandStatusViewSet, basename="land-status")
router.register("crops", CropViewSet, basename="crop")

urlpatterns = [
    path("", include(router.urls)),
    path("statistics/", CropStatisticsView.as_view(), name="crop-statistics"),
]
