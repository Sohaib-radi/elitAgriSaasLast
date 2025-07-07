from rest_framework.routers import DefaultRouter
from finance.views.debt import DebtViewSet
from django.urls import path

from finance.views.dept_attachement import DeptItemAttachmentUploadView


router = DefaultRouter()
router.register("", DebtViewSet, basename="debt")

urlpatterns = router.urls

urlpatterns = router.urls + [
    path("items/<int:pk>/upload-attachments/", DeptItemAttachmentUploadView.as_view(), name="dept-item-upload-attachments"),
]