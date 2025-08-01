# Generated by Django 5.1.7 on 2025-06-21 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0008_animal_is_purchased'),
        ('core', '0009_alter_invitetoken_farm_alter_person_farm_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', related_query_name='%(app_label)s_%(class)s', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='animalbirth',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', related_query_name='%(app_label)s_%(class)s', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='animaldeath',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', related_query_name='%(app_label)s_%(class)s', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AlterField(
            model_name='animallist',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', related_query_name='%(app_label)s_%(class)s', to='core.farm', verbose_name='Farm'),
        ),
    ]
