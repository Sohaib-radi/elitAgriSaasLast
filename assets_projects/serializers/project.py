from rest_framework import serializers
from django.db import transaction
from assets_projects.models.asset import Asset
from assets_projects.models.cost import ProjectCost
from assets_projects.serializers.asset import AssetCreateUpdateSerializer
from assets_projects.serializers.cost import ProjectCostCreateUpdateSerializer
from ..models.project import Project
from .base import FarmScopedSerializer
from django.utils.translation import gettext_lazy as _

class ProjectSerializer(FarmScopedSerializer):
    parent_project_name = serializers.CharField(
        source='parent_project.name',
        read_only=True
    )
    farm_name = serializers.CharField(
        source='farm.name',
        read_only=True
    )
    cost_count = serializers.IntegerField(
        source='costs.count',
        read_only=True
    )
    total_costs = serializers.DecimalField(
        source='get_total_costs',
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'parent_project', 'parent_project_name',
            'description', 'address', 'image', 'created_at', 'updated_at',
            'farm', 'farm_name', 'cost_count', 'total_costs'
        ]
        extra_kwargs = {
            'farm': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

class ProjectCreateUpdateSerializer(FarmScopedSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'parent_project', 'description', 
            'address', 'image'
        ]

    def validate_parent_project(self, value):
        """Ensure parent project belongs to same farm"""
        request = self.context.get('request')
        if value and request and value.farm != request.user.active_farm:
            raise serializers.ValidationError(
                _("Parent project must belong to the same farm")
            )
        return value

    def create(self, validated_data):
        validated_data = validated_data.copy()
        validated_data['farm'] = self.context['request'].user.active_farm
        return super().create(validated_data)


class ProjectDetailSerializer(ProjectSerializer):
    assets = AssetCreateUpdateSerializer(many=True, read_only=True)
    costs = ProjectCostCreateUpdateSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['assets', 'costs']


class ProjectWithAssetsAndCostsSerializer(serializers.Serializer):
    project = ProjectCreateUpdateSerializer()
    assets = AssetCreateUpdateSerializer(many=True, required=False)
    costs = ProjectCostCreateUpdateSerializer(many=True, required=False)

    def validate(self, data):
        request = self.context['request']
        farm = request.user.active_farm

        project_data = data.get("project", {}).copy()
        parent = project_data.get("parent_project")

        if parent and parent.farm != farm:
            raise serializers.ValidationError({
                'project.parent_project': "Parent project must belong to your farm"
            })

        # Step 1: Validate all assets and build temp asset map
        asset_map = {}
        for i, asset in enumerate(data.get("assets", [])):
            supplier = asset.get("supplier")
            if supplier and supplier.farm != farm:
                raise serializers.ValidationError({
                    f'assets[{i}].supplier': "Supplier must belong to your farm"
                })

            temp_id = asset.get("temp_id") or f"temp-{i}"
            asset_map[temp_id] = asset

        # Step 2: Validate all costs and asset references
        for j, cost in enumerate(data.get("costs", [])):
            asset_ref = cost.get("asset")
            if asset_ref:
                if isinstance(asset_ref, str):
                    if asset_ref not in asset_map:
                        raise serializers.ValidationError({
                            f'costs[{j}].asset': "Referenced asset does not exist in assets list"
                        })
                elif isinstance(asset_ref, int):
                    asset = Asset.objects.filter(id=asset_ref, farm=farm).first()
                    if not asset:
                        raise serializers.ValidationError({
                            f'costs[{j}].asset': "Asset does not exist or does not belong to your farm"
                        })

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        farm = request.user.active_farm

        project_data = validated_data.get('project', {}).copy()
        assets_data = validated_data.get('assets', [])
        costs_data = validated_data.get('costs', [])

        # Step 1: Create the project
        project_data.pop('farm', None)
        project = Project.objects.create(**project_data, farm=farm)

        # Step 2: Create assets and track temp_ids
        temp_id_to_asset = {}
        created_assets = []
        for asset_data in assets_data:
            asset_data = asset_data.copy()
            temp_id = asset_data.pop('temp_id', None)
            asset_data.pop('farm', None)

            asset = Asset.objects.create(
                **asset_data,
                farm=farm,
                project=project
            )

            if temp_id:
                temp_id_to_asset[temp_id] = asset

            created_assets.append(asset)

        # Step 3: Create costs with resolved asset references
        created_costs = []
        for cost_data in costs_data:
            cost_data = cost_data.copy()
            asset_ref = cost_data.pop('asset', None)
            resolved_asset = None

            if isinstance(asset_ref, str) and asset_ref.startswith('temp-'):
                resolved_asset = temp_id_to_asset.get(asset_ref)
            elif isinstance(asset_ref, int):
                resolved_asset = Asset.objects.filter(id=asset_ref, farm=farm).first()

            cost = ProjectCost.objects.create(
                name=cost_data.get('name'),
                amount=cost_data.get('amount'),
                description=cost_data.get('description'),
                project=project,
                asset=resolved_asset,
                farm=farm
            )
            created_costs.append(cost)

        self.instance = {
            'project': project,
            'assets': created_assets,
            'costs': created_costs
        }
        return self.instance

    def to_representation(self, instance):
        return {
            'project': ProjectCreateUpdateSerializer(instance['project'], context=self.context).data,
            'assets': AssetCreateUpdateSerializer(instance['assets'], many=True, context=self.context).data,
            'costs': ProjectCostCreateUpdateSerializer(instance['costs'], many=True, context=self.context).data,
        }

    def update(self, instance, validated_data):
        raise NotImplementedError("Update not supported in this serializer.")