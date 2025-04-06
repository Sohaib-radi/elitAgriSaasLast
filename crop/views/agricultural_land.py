from crop.filters import AgriculturalLandFilter
from crop.models.agricultural_land import AgriculturalLand
from crop.serializers.agricultural_land import AgriculturalLandSerializer
from django_filters.rest_framework import DjangoFilterBackend
from core.viewsets.base import AutoPermissionViewSet
import logging

logger = logging.getLogger(__name__)


class AgriculturalLandViewSet(AutoPermissionViewSet):
    """
    ViewSet to manage agricultural land linked to general land.
    """
    queryset = AgriculturalLand.objects.all()
    serializer_class = AgriculturalLandSerializer
    permission_module = "crop"
    filter_backends = [DjangoFilterBackend]
    filterset_class = AgriculturalLandFilter

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, "active_farm") or not user.active_farm:
            logger.warning(f"User {user} has no active_farm set.")
            return AgriculturalLand.objects.none()
        return self.queryset.filter(farm=user.active_farm)

    def perform_create(self, serializer):
        """
        Automatically set the current user's active_farm during creation.
        """
        serializer.save(farm=self.request.user.active_farm)
