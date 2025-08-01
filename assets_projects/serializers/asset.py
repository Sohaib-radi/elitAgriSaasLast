from rest_framework import serializers

from assets_projects.models.project import Project
from product_catalogue.models.supplier import Supplier
from ..models.asset import Asset
from .base import FarmScopedSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response


class AssetSerializer(FarmScopedSerializer):
    asset_type_display = serializers.CharField(
        source='get_asset_type_display',
        read_only=True
    )
    farm_name = serializers.CharField(
        source='farm.name',
        read_only=True
    )
    supplier_name = serializers.CharField(
        source='supplier.supplier_name',
        read_only=True,
        default=None
    )
    primary_project = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    primary_project_name = serializers.CharField(
        source='primary_project.name',
        read_only=True
    )
    shared_projects = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    shared_project_names = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'purchase_date', 'price', 'asset_type',
            'asset_type_display','asset_code', 'lifespan', 'description', 'supplier',
            'created_at', 'updated_at', 'supplier_name', 'farm', 'farm_name',
            'primary_project', 'primary_project_name',
            'shared_projects', 'shared_project_names'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'farm': {'read_only': True}
        }
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.primary_project or instance.shared_projects.exists():
            return Response(
                {"detail": _("Cannot delete this asset because it is linked to one or more projects.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    def update(self, instance, validated_data):
        # Prevent farm from being updated
        validated_data.pop('farm', None)
        return super().update(instance, validated_data)
    
    def get_shared_project_names(self, obj):
        return [project.name for project in obj.shared_projects.all()]

class AssetCreateUpdateSerializer(FarmScopedSerializer):
    temp_id = serializers.CharField(required=False, write_only=True)

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        required=False,
        allow_null=True
    )

    primary_project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        required=False,
        allow_null=True
    )

    shared_projects = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Asset
        fields = [
            "name", "purchase_date", "price", "asset_type", "lifespan",
            "primary_project", "shared_projects", "description", "supplier", "temp_id"
        ]
        extra_kwargs = {
            "primary_project": {"required": False},
            "shared_projects": {"required": False},
        }

    def validate_supplier(self, value):
        if value is None:
            return None

        farm = self.context['request'].user.active_farm
        if value.farm_id != farm.id:
            raise serializers.ValidationError("Supplier does not belong to the active farm.")

        return value

    def create(self, validated_data):
        validated_data['farm'] = self.context['request'].user.active_farm
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent farm overwrite
        validated_data.pop('farm', None)
        return super().update(instance, validated_data)
