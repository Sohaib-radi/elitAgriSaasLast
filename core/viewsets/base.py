from rest_framework.viewsets import ModelViewSet
from core.permissions.mixins import AutoPermissionMixin
from rest_framework.views import APIView

class AutoPermissionViewSet(AutoPermissionMixin, ModelViewSet):
    """
    Base viewset that uses AutoPermissionMixin to enforce central permission logic.
    """
    pass


class AutoPermissionAPIView(AutoPermissionMixin, APIView):
    """
    Base APIView that auto-applies permissions using the central permission registry.
    """
    pass