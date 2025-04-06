from land.models.wilaya import Wilaya
from land.serializers.wilaya import WilayaSerializer
from core.viewsets.base import AutoPermissionViewSet

class WilayaViewSet(AutoPermissionViewSet):
    serializer_class = WilayaSerializer
    permission_module = "wilayas"  # ✅ Must match key in PERMISSION_MAP
    queryset = Wilaya.objects.all().order_by("name")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
