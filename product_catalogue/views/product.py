

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions.permissions import IsFarmOwnerOrReadOnly, IsNotExpired, HasRolePermission
from product_catalogue.models import Product, ProductCategory, ProductVariant
from product_catalogue.serializers.product import ProductSerializer,ProductSerializer, ProductCategorySerializer, ProductVariantSerializer
from product_catalogue.models import ProductImage
from urllib.parse import urlparse
from product_catalogue.models import Product
from product_catalogue.serializers.product import ProductSerializer
from core.permissions.mixins import AutoPermissionMixin
from rest_framework.viewsets import ModelViewSet
from core.viewsets.base import AutoPermissionViewSet
from rest_framework.response import Response
from rest_framework import status
import json
from django.db.models import Q

class ProductViewSet(AutoPermissionViewSet):
    serializer_class = ProductSerializer
    permission_module = "products"

    def get_queryset(self):
        return Product.objects.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        serializer.save(farm=self.request.user.active_farm)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"products": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"product": serializer.data})

    def partial_update(self, request, *args, **kwargs):
        product = self.get_object()

        removed_images = request.data.get('removed_images', [])

        # Handle stringified list from FormData
        if isinstance(removed_images, str):
            removed_images = removed_images.strip()
            if removed_images:
                try:
                    removed_images = json.loads(removed_images)
                except json.JSONDecodeError:
                    removed_images = []
            else:
                removed_images = []

        # ✅ Remove by ID directly (no path parsing)
        if removed_images:
            ProductImage.objects.filter(product=product, id__in=removed_images).delete()

        # Continue with update
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"product": serializer.data}, status=status.HTTP_200_OK)



class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsNotExpired(),
            HasRolePermission("products.view"),
        ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"categories": serializer.data})  
    
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