from django.contrib import admin
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.db import models

# Get all models from the 'banking' app
app_models = apps.get_app_config('banking').get_models()

for model in app_models:
    class AutoAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]
        search_fields = [field.name for field in model._meta.fields if isinstance(field, models.CharField)]
        list_filter = [field.name for field in model._meta.fields if field.choices or isinstance(field, (models.BooleanField, models.DateField))]
        ordering = ['-id']
        readonly_fields = [f.name for f in model._meta.fields if f.auto_created and not f.editable]

    try:
        admin.site.register(model, AutoAdmin)
    except admin.sites.AlreadyRegistered:
        pass
