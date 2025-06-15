from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from product_catalogue.serializers.product import ProductImageSerializer
from core.viewsets.base import AutoPermissionViewSet
from product_catalogue.models import Product
from rest_framework import status


class ProductImageUploadView(AutoPermissionViewSet):
    permission_module = "products"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, farm=request.user.active_farm)
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)