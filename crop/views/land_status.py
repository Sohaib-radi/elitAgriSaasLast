from crop.filters import LandStatusFilter
from crop.models.land_status import LandStatus
from crop.serializers.land_status import LandStatusSerializer
from core.viewsets.base import AutoPermissionViewSet
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger(__name__)


class LandStatusViewSet(AutoPermissionViewSet):
    """
    ViewSet to manage the status of agricultural lands with filtering and scoped farm access.
    Permissions are automatically applied via AutoPermissionMixin based on permission_module.
    """
    permission_module = "crop"
    serializer_class = LandStatusSerializer
    queryset = LandStatus.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LandStatusFilter

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, "active_farm") or not user.active_farm:
            logger.warning(f"User {user} has no active_farm set.")
            return LandStatus.objects.none()
        return self.queryset.filter(farm=user.active_farm)

    def perform_create(self, serializer):
        """
        Automatically set the farm to user's active farm when creating a LandStatus.
        """
        serializer.save(farm=self.request.user.active_farm)
