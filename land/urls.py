from rest_framework.routers import DefaultRouter
from land.views.land import LandViewSet
from land.views.wilaya import WilayaViewSet
from land.views.purchase import LandPurchaseViewSet

router = DefaultRouter()
router.register("lands", LandViewSet, basename="lands")
router.register("wilayas", WilayaViewSet, basename="wilaya")
router.register("purchases", LandPurchaseViewSet, basename="land-purchases")


urlpatterns = router.urls
