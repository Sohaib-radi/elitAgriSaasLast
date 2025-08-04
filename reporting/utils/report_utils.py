import os
from django.conf import settings
from farm_settings.models.farm_settings import FarmSettings
from pathlib import Path
def get_farm_info(farm):
    try:
        settings_obj = FarmSettings.objects.get(farm=farm)
        logo = settings_obj.farm.logo

        return {
            "farm_name": settings_obj.legal_name,
            "logo_relative_path": logo.name if logo else None,  
            "logo_absolute_path": Path(settings.MEDIA_ROOT).joinpath(logo.name).resolve().as_uri() if logo else None,

            "address": settings_obj.address,
            "phone": settings_obj.telephone,
            "email": settings_obj.email,
        }
    except FarmSettings.DoesNotExist:
        return {
            "farm_name": "Unknown Farm",
            "logo_relative_path": None,
            "address": "",
            "phone": "",
            "email": "",
        }