from crop.filters import CropFilter
from crop.models.crop import Crop, CropStatusChoices
from crop.serializers.crop import CropSerializer
from warehouse.models.entry import WarehouseEntry
from warehouse.models.warehouse import Warehouse
from django.contrib.contenttypes.models import ContentType
from datetime import date
from core.viewsets.base import AutoPermissionViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError


class CropViewSet(AutoPermissionViewSet):
    """
    ViewSet to manage crop tracking per agricultural land, with auto warehouse integration.
    """
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_module = "crop"
    filter_backends = [DjangoFilterBackend]
    filterset_class = CropFilter

    def get_queryset(self):
        return self.queryset.filter(farm=self.request.user.active_farm)

    def perform_create(self, serializer):
        """
        Automatically assign farm when creating a new crop.
        """
        instance = serializer.save(farm=self.request.user.active_farm)

        # Automatically create a warehouse entry if the crop is already harvested
        if instance.status == CropStatusChoices.HARVESTED:
            if not instance.quantity or not instance.unit:
                raise ValidationError("Quantity and unit are required to store in warehouse.")
            if not self.select_default_warehouse(instance.farm):
                raise ValidationError("No default warehouse found for this farm.")

            already_exists = WarehouseEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(Crop),
                object_id=instance.id,
                farm=instance.farm
            ).exists()

            if not already_exists:
                WarehouseEntry.objects.create(
                    warehouse=self.select_default_warehouse(instance.farm),
                    content_object=instance,
                    quantity=instance.quantity,
                    unit=instance.unit,
                    date_added=date.today(),
                    farm=instance.farm
                )

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == CropStatusChoices.HARVESTED:
            if not instance.quantity or not instance.unit:
                raise ValidationError("Quantity and unit are required to store in warehouse.")
            if not self.select_default_warehouse(instance.farm):
                raise ValidationError("No default warehouse found for this farm.")

            already_exists = WarehouseEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(Crop),
                object_id=instance.id,
                farm=instance.farm
            ).exists()

            if not already_exists:
                WarehouseEntry.objects.create(
                    warehouse=self.select_default_warehouse(instance.farm),
                    content_object=instance,
                    quantity=instance.quantity,
                    unit=instance.unit,
                    date_added=date.today(),
                    farm=instance.farm
                )

    def select_default_warehouse(self, farm):
        return Warehouse.objects.filter(farm=farm).first()
