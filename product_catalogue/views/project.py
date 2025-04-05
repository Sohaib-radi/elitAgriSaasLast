from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from product_catalogue.models.project import Project
from product_catalogue.serializers.project import ProjectSerializer
from core.permissions.permissions import IsFarmOwnerOrReadOnly
from core.viewsets.base import AutoPermissionViewSet

class ProjectViewSet(AutoPermissionViewSet):
    """
    Manage projects for the active farm.
    """
    serializer_class = ProjectSerializer
    permission_module = "projects"

    def get_queryset(self):
        return Project.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )
