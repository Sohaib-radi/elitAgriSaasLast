from django.urls import path, include
from rest_framework.routers import DefaultRouter

from assets_projects.views.asset_views import AssetViewSet
from assets_projects.views.cost_views import ProjectCostViewSet
from assets_projects.views.project_views import ProjectViewSet


router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'costs', ProjectCostViewSet, basename='projectcost')

urlpatterns = [
    path('', include(router.urls)),
]