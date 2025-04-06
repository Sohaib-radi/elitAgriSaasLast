from django.apps import AppConfig


class FarmSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farm_settings"

    def ready(self):
        import farm_settings.signals
