from django.urls import path, include

urlpatterns = [
    path("animal/", include("reporting.urls.animal_urls")),
    path("report/", include("reporting.urls.report_urls")),
]