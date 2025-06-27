from rest_framework import serializers
from ..models.asset import Asset
from .base import FarmScopedSerializer
from django.utils.translation import gettext_lazy as _

class AssetSerializer(FarmScopedSerializer):
    asset_type_display = serializers.CharField(
        source='get_asset_type_display',
        read_only=True
    )
    farm_name = serializers.CharField(
        source='farm.name',
        read_only=True
    )
    
    class Meta:
        model = Asset
        fields = [
            'id', 'name', 'purchase_date', 'price', 'asset_type',
            'asset_type_display', 'lifespan', 'description', 'supplier',
            'created_at', 'updated_at', 'farm', 'farm_name'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'farm': {'read_only': True}  # Farm is auto-set from context
        }

class AssetCreateUpdateSerializer(FarmScopedSerializer):
    class Meta:
        model = Asset
        fields = [
            'name', 'purchase_date', 'price', 'asset_type',
            'lifespan', 'description', 'supplier'
        ]
    
    def validate(self, data):
        data = super().validate(data)

        if 'supplier' in data:
            from product_catalogue.models import Supplier
            try:
                supplier = Supplier.objects.get(
                    id=data['supplier'].id if isinstance(data['supplier'], Supplier) else data['supplier'],
                    farm=self.context['request'].user.active_farm
                )
            except Supplier.DoesNotExist:
                raise serializers.ValidationError({
                    'supplier': _('Supplier does not exist or belongs to a different farm')
                })
            data['supplier'] = supplier
            
        return data

    def create(self, validated_data):
        """
        Ensure farm is set from context, not from input data
        """
        validated_data['farm'] = self.context['request'].user.active_farm
        return super().create(validated_data)