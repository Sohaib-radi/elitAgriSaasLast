from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework import status
import logging

from product_catalogue.models.personal_product import PersonalProduct
from product_catalogue.serializers.personal_product import PersonalProductCreateSerializer
from core.viewsets.base import AutoPermissionViewSet
from product_catalogue.serializers.personal_product import PersonalProductSerializer
from product_catalogue.serializers.project import ProjectSerializer
from product_catalogue.serializers.product import ProductSerializer


logger = logging.getLogger(__name__)

class PersonalProductViewSet(AutoPermissionViewSet):
    queryset = PersonalProduct.objects.all()
    permission_module = "products"

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonalProductCreateSerializer
        return PersonalProductSerializer
    
class PersonalProductCreateAPIView(AutoPermissionViewSet):
    queryset = PersonalProduct.objects.all()
    serializer_class = PersonalProductCreateSerializer
    permission_module = "products"
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'personal_product_create'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        personal_product = serializer.save()

        logger.info(
            f"[PersonalProduct Created] User={request.user.username} | "
            f"Farm={request.user.active_farm_id} | "
            f"Project={personal_product.project_id} | Product={personal_product.product_id}"
        )

        response_data = {
            "message": ("✅ Personal product created successfully."),
            "personal_product": PersonalProductSerializer(personal_product).data,
            "project": ProjectSerializer(personal_product.project).data,
            "product": ProductSerializer(personal_product.product).data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
