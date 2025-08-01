from django.apps import AppConfig


class AssetsProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assets_projects'
    def ready(self):
        import assets_projects.signals
    
