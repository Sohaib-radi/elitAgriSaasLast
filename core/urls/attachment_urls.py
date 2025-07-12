from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.attachment_view import AttachmentViewSet

router = DefaultRouter()
router.register(r"attachments", AttachmentViewSet, basename="attachment")

urlpatterns = [
    path("", include(router.urls)),
]
