# Generated by Django 5.1.7 on 2025-04-04 01:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('animal', '0001_initial'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='animal',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AddField(
            model_name='animal',
            name='father',
            field=models.ForeignKey(blank=True, help_text='Reference to the father animal.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fathered_animals', to='animal.animal', verbose_name='Father'),
        ),
        migrations.AddField(
            model_name='animal',
            name='mother',
            field=models.ForeignKey(blank=True, help_text='Reference to the mother animal.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mothered_animals', to='animal.animal', verbose_name='Mother'),
        ),
        migrations.AddField(
            model_name='animalbirth',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='animalbirth',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AddField(
            model_name='animalbirth',
            name='father',
            field=models.ForeignKey(blank=True, help_text='The father animal (optional).', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='births_as_father', to='animal.animal', verbose_name='Father'),
        ),
        migrations.AddField(
            model_name='animalbirth',
            name='mother',
            field=models.ForeignKey(blank=True, help_text='The mother animal.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='births_as_mother', to='animal.animal', verbose_name='Mother'),
        ),
        migrations.AddField(
            model_name='animalcustomfieldvalue',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_field_values', to='animal.animal'),
        ),
        migrations.AddField(
            model_name='animalcustomfieldvalue',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='animaldeath',
            name='animal',
            field=models.ForeignKey(help_text='Animal that has died.', on_delete=django.db.models.deletion.CASCADE, related_name='deaths', to='animal.animal', verbose_name='Animal'),
        ),
        migrations.AddField(
            model_name='animaldeath',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='animaldeath',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AddField(
            model_name='animaldeathimage',
            name='death',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='animal.animaldeath', verbose_name='Death Record'),
        ),
        migrations.AddField(
            model_name='animalimage',
            name='animal',
            field=models.ForeignKey(help_text='The animal this image belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='animal.animal', verbose_name='Animal'),
        ),
        migrations.AddField(
            model_name='animalimage',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='animallist',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='animallist',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='core.farm', verbose_name='Farm'),
        ),
        migrations.AddField(
            model_name='animalbirth',
            name='list',
            field=models.ForeignKey(help_text='The list the animal will be moved to after birth.', on_delete=django.db.models.deletion.CASCADE, related_name='births', to='animal.animallist', verbose_name='Animal List'),
        ),
        migrations.AddField(
            model_name='animal',
            name='list',
            field=models.ForeignKey(help_text='The custom list/category the animal is part of.', on_delete=django.db.models.deletion.CASCADE, related_name='animals', to='animal.animallist', verbose_name='Animal List'),
        ),
        migrations.AddField(
            model_name='animalvaccine',
            name='animal',
            field=models.ForeignKey(help_text='The animal receiving the vaccine.', on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='animal.animal', verbose_name='Animal'),
        ),
        migrations.AddField(
            model_name='animalvaccine',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='customlistfield',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='customlistfield',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_fields', to='animal.animallist', verbose_name='Animal List'),
        ),
        migrations.AddField(
            model_name='animalcustomfieldvalue',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animal.customlistfield'),
        ),
        migrations.AlterUniqueTogether(
            name='vaccinerecommendation',
            unique_together={('species', 'vaccine_name', 'recommended_age_days')},
        ),
        migrations.AlterUniqueTogether(
            name='animallist',
            unique_together={('farm', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='animal',
            unique_together={('farm', 'animal_number')},
        ),
        migrations.AlterUniqueTogether(
            name='animalvaccine',
            unique_together={('animal', 'name', 'date_given')},
        ),
        migrations.AlterUniqueTogether(
            name='animalcustomfieldvalue',
            unique_together={('animal', 'field')},
        ),
    ]
