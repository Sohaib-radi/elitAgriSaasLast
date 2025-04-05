from rest_framework import viewsets
from core.viewsets.base import AutoPermissionViewSet
from product_catalogue.models.supplier import SupplierList, Supplier
from product_catalogue.serializers.supplier import SupplierListSerializer, SupplierSerializer

class SupplierListViewSet(AutoPermissionViewSet, viewsets.ModelViewSet):
    """
    Manage supplier lists for the farm.
    """
    serializer_class = SupplierListSerializer
    permission_module = "suppliers"

    def get_queryset(self):
        return SupplierList.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )

class SupplierViewSet(AutoPermissionViewSet):
    """
    Manage individual suppliers for a given product and list.
    """
    serializer_class = SupplierSerializer
    permission_module = "suppliers"

    def get_queryset(self):
        return Supplier.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(
            farm=self.request.user.active_farm,
            created_by=self.request.user
        )
