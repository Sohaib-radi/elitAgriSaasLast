from django.urls import path, include

urlpatterns = [
    path("", include("core.urls.person_urls")),
    path("", include("core.urls.attachment_urls")),
]