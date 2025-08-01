# Generated by Django 5.1.7 on 2025-07-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0010_animalvaccine_farm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='description',
            field=models.TextField(blank=True, help_text='Additional notes or remarks, or Circumstances of animal loss in case of lost', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='status',
            field=models.CharField(choices=[('pregnant', 'Pregnant'), ('with_baby', 'With Baby'), ('not_pregnant', 'Not Pregnant'), ('healthy', 'Healthy'), ('sick', 'Sick'), ('deceased', 'Deceased'), ('lost', 'Lost')], default='healthy', help_text='Current health or reproductive status.', max_length=20, verbose_name='Status'),
        ),
    ]
