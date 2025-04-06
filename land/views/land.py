from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from land.models.land import Land
from land.serializers.land import LandSerializer
from land.filters.land import LandFilter
from core.viewsets.base import AutoPermissionViewSet

class LandViewSet(AutoPermissionViewSet):
    """
    Manage all land records for the active farm
    """
    serializer_class = LandSerializer
    permission_module = "lands"  # 👈 must match key in your PERMISSION_MAP
    filter_backends = [DjangoFilterBackend]
    filterset_class = LandFilter

    def get_queryset(self):
        return Land.objects.filter(farm=self.request.user.active_farm).select_related("wilaya")

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )
