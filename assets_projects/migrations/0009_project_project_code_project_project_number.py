# Generated by Django 5.1.7 on 2025-07-25 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_projects', '0008_projectcost_cost_type_alter_asset_asset_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_code',
            field=models.CharField(editable=False, max_length=100, null=True, unique=True, verbose_name='Project Code'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Project Number'),
        ),
    ]
