# Generated by Django 5.1.7 on 2025-07-25 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_projects', '0009_project_project_code_project_project_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_code',
            field=models.CharField(default=1, editable=False, max_length=100, unique=True, verbose_name='Project Code'),
            preserve_default=False,
        ),
    ]
