from rest_framework.routers import DefaultRouter
from finance.views.debt import DebtViewSet

router = DefaultRouter()
router.register("", DebtViewSet, basename="debt")

urlpatterns = router.urls