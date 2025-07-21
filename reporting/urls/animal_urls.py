from django.urls import path
from reporting.views.animal_report_views import AnimalDeathReportView

urlpatterns = [
    path("animal-death/", AnimalDeathReportView.as_view(), name="animal-death-report"),
]
