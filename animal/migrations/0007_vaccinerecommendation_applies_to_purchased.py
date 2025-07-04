# Generated by Django 5.1.7 on 2025-05-31 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0006_alter_animalvaccine_applies_to_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccinerecommendation',
            name='applies_to_purchased',
            field=models.BooleanField(default=False, help_text='Whether this vaccine should be applied to purchased animals.', verbose_name='Applies to Purchased Animals'),
        ),
    ]
