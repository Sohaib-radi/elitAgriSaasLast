from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from core.permissions.permissions import IsFarmAdmin
from farm_settings.models import FarmSettings
from farm_settings.serializers import FarmSettingsSerializer
from core.models.farm import Farm
from django.utils.translation import gettext_lazy as _
from core.viewsets.base import AutoPermissionAPIView 

class FarmSettingsAdminViewSet(viewsets.ModelViewSet):
    """
    Full admin control over all farm settings
    """
    queryset = FarmSettings.objects.all()
    serializer_class = FarmSettingsSerializer
    permission_classes = [IsAdminUser]

class MyFarmSettingsView(AutoPermissionAPIView):
    """
    Get or update settings for the current farm of the authenticated user
    """
    permission_module = "farm_settings"
    parser_classes = [MultiPartParser, FormParser]

    def get_farm_settings(self, request):
        farm = getattr(request.user, "active_farm", None)
        if not farm or not hasattr(farm, "settings"):
            return None
        return farm.settings

    def get(self, request):
        settings = self.get_farm_settings(request)
        if not settings:
            return Response({"detail": _("Settings not found.")}, status=404)

        serializer = FarmSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings = self.get_farm_settings(request)
        if not settings:
            return Response({"detail": _("Settings not found.")}, status=404)

        serializer = FarmSettingsSerializer(settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Farm settings updated successfully."), "data": serializer.data})

    def patch(self, request):
        settings = self.get_farm_settings(request)
        if not settings:
            return Response({"detail": _("Settings not found.")}, status=404)

        serializer = FarmSettingsSerializer(settings, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Farm settings partially updated."), "data": serializer.data})


class FarmSettingsListView(AutoPermissionAPIView):
    """
    Get settings of a specific farm (admin only)
    """
    permission_module = "farm_settings"

    def get(self, request, farm_id=None):
        if not farm_id:
            return Response({"detail": _("Farm ID is required.")}, status=400)

        try:
            farm = Farm.objects.get(id=farm_id)
        except Farm.DoesNotExist:
            return Response({"detail": _("Farm not found.")}, status=404)

        if not hasattr(farm, "settings"):
            return Response({"detail": _("Settings not found for this farm.")}, status=404)

        serializer = FarmSettingsSerializer(farm.settings)
        return Response(serializer.data)
