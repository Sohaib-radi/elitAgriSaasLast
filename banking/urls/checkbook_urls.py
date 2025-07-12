from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views.checkbook_view import CheckbookViewSet

router = DefaultRouter()
router.register(r"checkbooks", CheckbookViewSet, basename="checkbook")

urlpatterns = [
    path("", include(router.urls)),
]
