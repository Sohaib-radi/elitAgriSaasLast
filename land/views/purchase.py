from rest_framework import permissions
from land.models.purchase import LandPurchase
from land.serializers.purchase import LandPurchaseSerializer
from core.viewsets.base import AutoPermissionViewSet

class LandPurchaseViewSet(AutoPermissionViewSet):
    """
    Manage land purchase and sale records
    """
    serializer_class = LandPurchaseSerializer
    permission_module = "land_purchases"  
    
    def get_queryset(self):
        return LandPurchase.objects.filter(land__farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
