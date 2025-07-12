from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.reconciliation_view import ReconciliationViewSet

router = DefaultRouter()
router.register(r"reconciliations", ReconciliationViewSet, basename="reconciliation")

urlpatterns = [
    path("", include(router.urls)),
]
