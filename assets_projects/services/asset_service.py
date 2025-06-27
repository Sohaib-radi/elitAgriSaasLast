from django.core.exceptions import ObjectDoesNotExist
from ..models.asset import Asset

class AssetService:
    @staticmethod
    def get_all_assets():
        return Asset.objects.all()  # Base queryset - filtering happens in view
    
    @staticmethod
    def get_asset_by_id(asset_id):
        try:
            return Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return None
    
    @staticmethod
    def create_asset(asset_data):
        asset = Asset(**asset_data)
        asset.full_clean()
        asset.save()
        return asset
    
    @staticmethod
    def update_asset(asset_id, asset_data):
        asset = AssetService.get_asset_by_id(asset_id)
        if asset:
            for field, value in asset_data.items():
                setattr(asset, field, value)
            asset.full_clean()
            asset.save()
        return asset
    
    @staticmethod
    def delete_asset(asset_id):
        asset = AssetService.get_asset_by_id(asset_id)
        if asset:
            asset.delete()
            return True
        return False