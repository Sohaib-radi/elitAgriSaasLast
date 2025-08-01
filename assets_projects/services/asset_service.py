from django.core.exceptions import ObjectDoesNotExist
from ..models.asset import Asset
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class AssetService:
    @staticmethod
    def get_all_assets():
        return Asset.objects.all()  # Filtering happens in views
    
    @staticmethod
    def get_asset_by_id(asset_id):
        try:
            return Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return None

    @staticmethod
    def create_asset(asset_data: dict) -> Asset:
        shared_projects = asset_data.pop("shared_projects", [])

        asset = Asset(**asset_data)
        asset.full_clean()
        asset.save()

        if shared_projects:
            asset.shared_projects.set(shared_projects)

        return asset

    @staticmethod
    def update_asset(asset_id, asset_data):
        shared_projects = asset_data.pop("shared_projects", None)

        # 🔒 Ensure 'farm' is not updated here either
        asset_data.pop("farm", None)

        asset = AssetService.get_asset_by_id(asset_id)
        if asset:
            for field, value in asset_data.items():
                setattr(asset, field, value)

            asset.full_clean()
            asset.save()

            if shared_projects is not None:
                asset.shared_projects.set(shared_projects)

        return asset


    @staticmethod
    def delete_asset(asset_id: int):
        asset = Asset.objects.get(pk=asset_id)

        # Check for project associations before deletion
        if asset.primary_project or asset.shared_projects.exists():
            raise ValidationError(_("Cannot delete this asset because it is linked to one or more projects."))

        asset.delete()
