# Generated by Django 5.1.7 on 2025-04-14 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm_settings', '0002_farmsettings_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmsettings',
            name='logo',
        ),
    ]
