from rest_framework import serializers
from django.db import transaction
from assets_projects.models.asset import Asset
from assets_projects.models.cost import ProjectCost
from assets_projects.serializers.asset import AssetCreateUpdateSerializer
from assets_projects.serializers.cost import ProjectCostCreateUpdateSerializer
from product_catalogue.models.supplier import Supplier
from ..models.project import Project
from .base import FarmScopedSerializer
from django.utils.translation import gettext_lazy as _
import json


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
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    start_date = serializers.DateField(
        read_only=True
    )
    end_date = serializers.DateField(
        read_only=True
    )

    primary_image_url = serializers.SerializerMethodField()

    def get_primary_image_url(self, obj):
        request = self.context.get('request')
        image = obj.get_primary_image()
        if image and image.file:
            if request:
                return request.build_absolute_uri(image.file.url)
            return image.file.url  # fallback to relative if no request
        return None

    class Meta:
        model = Project
        fields = [
            'id', 'name','project_number', 'parent_project', 'parent_project_name',
            'description', 'address', 'created_at', 'updated_at',
            'farm', 'farm_name', 'cost_count', 'total_costs',
            'start_date', 'end_date',
            'is_active', 'primary_image_url'
        ]
        extra_kwargs = {
            'farm': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'project_number': {'read_only': True},
        }
class ProjectCreateUpdateSerializer(FarmScopedSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 'parent_project', 'description', 
            'address'
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
    project = serializers.JSONField()
    assets = serializers.JSONField(required=False)
    costs = serializers.JSONField(required=False)

    def validate(self, data):
        request = self.context["request"]
        self.farm = request.user.active_farm  # Store farm at serializer level

        # Validate project - ensure farm isn't in the data
        project_data = data["project"].copy()
        project_data.pop('farm', None)  # Remove farm if present
        
        project_serializer = ProjectCreateUpdateSerializer(
            data=project_data, 
            context=self.context
        )
        project_serializer.is_valid(raise_exception=True)
        self.validated_project = project_serializer.validated_data

        # Validate assets
        self.temp_id_to_asset_data = {}
        validated_assets = []
        raw_assets = data.get("assets", [])

        for i, asset_data in enumerate(raw_assets):
            # Remove farm if present in asset data
            asset_data_copy = asset_data.copy()
            asset_data_copy.pop('farm', None)
            
            serializer = AssetCreateUpdateSerializer(
                data=asset_data_copy, 
                context=self.context
            )
            serializer.is_valid(raise_exception=True)
            validated = serializer.validated_data

            # Handle supplier
            if 'supplier' in asset_data:
                supplier_id = asset_data['supplier']
                if supplier_id is not None:
                    supplier = Supplier.objects.filter(id=supplier_id, farm=self.farm).first()
                    if not supplier:
                        raise serializers.ValidationError({
                            f"assets[{i}].supplier": ["Invalid supplier"]
                        })
                    validated["supplier"] = supplier
                else:
                    validated["supplier"] = None

            # Store temp_id mapping
            temp_id = asset_data.get("temp_id")
            if temp_id:
                self.temp_id_to_asset_data[str(temp_id)] = validated

            validated_assets.append(validated)

        self.validated_assets = validated_assets

        # Validate costs
        validated_costs = []
        raw_costs = data.get("costs", [])

        for cost_data in raw_costs:
            serializer = ProjectCostCreateUpdateSerializer(
                data=cost_data, 
                context=self.context
            )
            serializer.is_valid(raise_exception=True)
            validated = serializer.validated_data
            
            # Store asset reference for later resolution
            if 'asset' in cost_data:
                validated['_asset_ref'] = cost_data['asset']
            
            validated_costs.append(validated)

        self.validated_costs = validated_costs
        return data

    @transaction.atomic
    def create(self, validated_data):
        # Create project
        project = Project.objects.create(**self.validated_project)

        # ✅ Handle uploaded images manually
        request = self.context['request']
        images = request.FILES.getlist("project.images")
        if images:
            from core.models import Attachment
            from django.contrib.contenttypes.models import ContentType

            content_type = ContentType.objects.get_for_model(Project)
            for image in images:
                Attachment.objects.create(
                    file=image,
                    content_type=content_type,
                    object_id=project.id,
                    file_type='image',
                    uploaded_by=request.user
                )

        # Create assets
        temp_id_to_asset = {}
        created_assets = []
        for asset_data in self.validated_assets:
            create_data = asset_data.copy()
            temp_id = create_data.pop('temp_id', None)

            shared_projects_ids = create_data.pop('shared_projects', [])

            # Assign primary project
            asset = Asset.objects.create(**create_data, primary_project=project)

            # Optional shared projects
            if shared_projects_ids:
                asset.shared_projects.set(shared_projects_ids)

            if temp_id:
                temp_id_to_asset[str(temp_id)] = asset
            created_assets.append(asset)

        # Create costs
        created_costs = []
        for cost_data in self.validated_costs:
            asset_ref = cost_data.pop('_asset_ref', None)
            resolved_asset = None

            if asset_ref is not None:
                resolved_asset = temp_id_to_asset.get(str(asset_ref))
                if not resolved_asset and str(asset_ref).isdigit():
                    try:
                        resolved_asset = Asset.objects.get(id=int(asset_ref), farm=self.farm)
                    except Asset.DoesNotExist:
                        pass

            cost = ProjectCost.objects.create(
                name=cost_data['name'],
                amount=cost_data['amount'],
                description=cost_data.get('description', ''),
                cost_type=cost_data.get('cost_type', 'other'),
                asset=resolved_asset,
                project=project,
                farm=self.farm
            )
            created_costs.append(cost)

        return {
            "project": project,
            "assets": created_assets,
            "costs": created_costs,
        }
    def to_representation(self, instance):
        return {
            "project": ProjectCreateUpdateSerializer(instance["project"], context=self.context).data,
            "assets": AssetCreateUpdateSerializer(instance["assets"], many=True, context=self.context).data,
            "costs": ProjectCostCreateUpdateSerializer(instance["costs"], many=True, context=self.context).data,
        }