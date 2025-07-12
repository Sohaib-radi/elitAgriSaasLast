from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.check_view import CheckViewSet

router = DefaultRouter()
router.register(r"checks", CheckViewSet, basename="check")

urlpatterns = [
    path("", include(router.urls)),
]
