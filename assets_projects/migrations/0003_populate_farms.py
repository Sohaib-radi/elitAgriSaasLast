


from django.db import migrations

def set_default_farm(apps, schema_editor):
    Asset = apps.get_model('assets_projects', 'Asset')
    Project = apps.get_model('assets_projects', 'Project')
    ProjectCost = apps.get_model('assets_projects', 'ProjectCost')
    Farm = apps.get_model('core', 'Farm')
    
    # Get or create default farm
    farm = Farm.objects.first()
    if not farm:
        farm = Farm.objects.create(name="Default Farm")
    
    # Update all null farms
    Asset.objects.filter(farm__isnull=True).update(farm=farm)
    Project.objects.filter(farm__isnull=True).update(farm=farm)
    ProjectCost.objects.filter(farm__isnull=True).update(farm=farm)

class Migration(migrations.Migration):
    dependencies = [
        ('assets_projects', '0002_temp_nullable_farm'),
    ]

    operations = [
        migrations.RunPython(set_default_farm),
    ]