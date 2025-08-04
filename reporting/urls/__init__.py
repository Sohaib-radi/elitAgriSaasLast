from django.urls import path, include


urlpatterns = [
    path("animal/", include("reporting.urls.animal_urls")),
    path("report/", include("reporting.urls.report_urls")),
    path("projects/", include("reporting.urls.project_urls")),
    path("finance/", include("reporting.urls.finance_urls")),
]
