from django.urls import path
from reporting.views.animal_birth_report_view import AnimalBirthReportView
from reporting.views.animal_report_view import AnimalReportView
from reporting.views.animal_report_views import AnimalDeathReportView
from reporting.views.animal_vaccine_report_view import AnimalVaccineReportView

urlpatterns = [
    path("animal-death/", AnimalDeathReportView.as_view(), name="animal-death-report"),
    path("animal-birth/", AnimalBirthReportView.as_view(), name="animal-birth-report"),
    path("animal-list/", AnimalReportView.as_view(), name="animal-report"),
     path("animal-vaccine/", AnimalVaccineReportView.as_view(), name="animal-vaccine-report"),
]
