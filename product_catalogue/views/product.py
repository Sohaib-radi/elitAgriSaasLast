

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsFarmOwnerOrReadOnly, IsNotExpired, HasRolePermission
from product_catalogue.models import Product, ProductCategory, ProductVariant
from product_catalogue.serializers.product import ProductSerializer,ProductSerializer, ProductCategorySerializer, ProductVariantSerializer


from product_catalogue.models import Product
from product_catalogue.serializers.product import ProductSerializer
from core.permissions.mixins import AutoPermissionMixin
from rest_framework.viewsets import ModelViewSet
from core.viewsets.base import AutoPermissionViewSet

class ProductViewSet(AutoPermissionViewSet):
    serializer_class = ProductSerializer
    permission_module = "products"
   
    
    def get_queryset(self):
        return Product.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(farm=self.request.user.active_farm)

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsNotExpired(),
            HasRolePermission("products.view"),  
        ]
    
class ProductVariantViewSet(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsNotExpired(),
            HasRolePermission("products.manage"),
        ]

    def get_queryset(self):
        return ProductVariant.objects.filter(product__farm=self.request.user.active_farm)