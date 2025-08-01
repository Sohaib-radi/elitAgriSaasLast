from django.urls import path
from reporting.views.project_detail_report_view import ProjectDetailReportView
from reporting.views.project_report_view import ProjectReportView


urlpatterns = [
     path("project-list/", ProjectReportView.as_view(), name="project-report"),
     path("detail/", ProjectDetailReportView.as_view(), name="project-detail-report"),
]
