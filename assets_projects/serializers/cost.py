from rest_framework import serializers
from ..models.cost import ProjectCost
from .base import FarmScopedSerializer
from django.utils.translation import gettext_lazy as _

class ProjectCostSerializer(FarmScopedSerializer):
    asset = serializers.SerializerMethodField()  # <-- override it
    asset_details = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='project.name', read_only=True)
    farm_name = serializers.CharField(source='farm.name', read_only=True)

    class Meta:
        model = ProjectCost
        fields = [
            'id', 'name', 'project', 'project_name',
            'asset', 'asset_details', 'amount', 'description',
            'created_at', 'updated_at', 'farm', 'farm_name'
        ]
        extra_kwargs = {
            'farm': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def get_asset(self, obj):
        return obj.asset.id if obj.asset else None

    def get_asset_details(self, obj):
        if not obj.asset:
            return None
        from .asset import AssetSerializer
        return AssetSerializer(obj.asset, context=self.context).data
    


class ProjectCostCreateUpdateSerializer(FarmScopedSerializer):
    # Allow asset to be a string or null (temporary ID or real ID handled manually in parent)
    asset = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = ProjectCost
        fields = ['name', 'project', 'asset', 'amount', 'description']
        extra_kwargs = {
            'project': {'required': False}  # ✅ Allow project to be set later in parent serializer
        }

    def validate(self, data):
        data = super().validate(data)
        request = self.context['request']
        farm = request.user.active_farm

        # Allow missing project if it's being nested (will be injected in parent serializer)
        project = data.get('project') or (self.instance.project if self.instance else None)
        if not project and self.instance is None:
            return data

        if not project:
            raise serializers.ValidationError({
                'project': _("Project is required")
            })

        if project.farm != farm:
            raise serializers.ValidationError({
                'project': _("Project does not belong to your farm")
            })

        # If asset is a string (temporary), skip farm validation — it's handled in parent
        asset = data.get('asset')
        if isinstance(asset, str):
            return data

        if asset and hasattr(asset, 'farm') and asset.farm != farm:
            raise serializers.ValidationError({
                'asset': _("Asset does not belong to your farm")
            })

        return data

    def create(self, validated_data):
        validated_data['farm'] = self.context['request'].user.active_farm
        return super().create(validated_data)