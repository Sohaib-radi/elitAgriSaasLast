from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reporting.views.report_view import ReportRecordViewSet

router = DefaultRouter()
router.register("records", ReportRecordViewSet, basename="report-record")

urlpatterns = [
    path("", include(router.urls)),
]
