# Generated by Django 5.1.7 on 2025-07-25 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_projects', '0007_project_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcost',
            name='cost_type',
            field=models.CharField(choices=[('agricultural', 'Agricultural'), ('animal', 'Animal'), ('construction', 'Construction'), ('warehouse', 'Warehouse'), ('irrigation', 'Irrigation'), ('greenhouse', 'Greenhouse'), ('agriculture', 'Agriculture'), ('land_development', 'Land Development'), ('soil_improvement', 'Soil Improvement'), ('animal_husbandry', 'Animal Husbandry'), ('veterinary', 'Veterinary'), ('barn_construction', 'Barn Construction'), ('equipment_purchase', 'Equipment Purchase'), ('transportation', 'Transportation'), ('electricity', 'Electricity'), ('transport', 'Transport'), ('maintenance', 'Maintenance'), ('processing', 'Processing'), ('research', 'Research'), ('tools', 'Tools'), ('administration', 'Administration'), ('other', 'Other')], default='other', max_length=20, verbose_name='Cost Type'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('agricultural', 'Agricultural'), ('animal', 'Animal'), ('construction', 'Construction'), ('warehouse', 'Warehouse'), ('irrigation', 'Irrigation'), ('greenhouse', 'Greenhouse'), ('agriculture', 'Agriculture'), ('land_development', 'Land Development'), ('soil_improvement', 'Soil Improvement'), ('animal_husbandry', 'Animal Husbandry'), ('veterinary', 'Veterinary'), ('barn_construction', 'Barn Construction'), ('equipment_purchase', 'Equipment Purchase'), ('transportation', 'Transportation'), ('electricity', 'Electricity'), ('transport', 'Transport'), ('maintenance', 'Maintenance'), ('processing', 'Processing'), ('research', 'Research'), ('tools', 'Tools'), ('administration', 'Administration'), ('other', 'Other')], max_length=20, verbose_name='Usage Type'),
        ),
    ]
