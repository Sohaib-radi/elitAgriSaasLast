from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.person import PersonViewSet

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='person')

urlpatterns = router.urls
