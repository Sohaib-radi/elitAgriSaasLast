# Generated by Django 5.1.7 on 2025-07-06 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0009_alter_animal_farm_alter_animalbirth_farm_and_more'),
        ('core', '0009_alter_invitetoken_farm_alter_person_farm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalvaccine',
            name='farm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', related_query_name='%(app_label)s_%(class)s', to='core.farm', verbose_name='Farm'),
            preserve_default=False,
        ),
    ]
