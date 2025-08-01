# Generated by Django 5.1.7 on 2025-05-31 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0007_vaccinerecommendation_applies_to_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='is_purchased',
            field=models.BooleanField(default=False, help_text='Indicates whether this animal was purchased from outside.', verbose_name='Is Purchased'),
        ),
    ]
