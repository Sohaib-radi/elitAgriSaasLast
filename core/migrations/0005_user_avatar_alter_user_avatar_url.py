# Generated by Django 5.1.7 on 2025-04-13 04:47

import core.models.user
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_address_user_avatar_url_user_city_user_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.user.user_avatar_upload_path, verbose_name='Profile Image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True, null=True, verbose_name='Avatar URL (external)'),
        ),
    ]
