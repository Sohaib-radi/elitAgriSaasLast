from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from product_catalogue.models.personal_product import PersonalProduct
from product_catalogue.serializers.personal_product import PersonalProductSerializer
from core.permissions.permissions import IsNotExpired
from core.viewsets.base import AutoPermissionViewSet

class PersonalProductViewSet(AutoPermissionViewSet):
    """
    Manage personal products linked to projects in the active farm.
    """
    serializer_class = PersonalProductSerializer
    permission_module = "personal_products"
   

    def get_queryset(self):
        return PersonalProduct.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )
