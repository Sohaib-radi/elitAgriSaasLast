from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),  # Ensure this exists for Farm model
        ('assets_projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='farm',
            field=models.ForeignKey(
                'core.Farm',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,  # Temporary allow null
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='farm',
            field=models.ForeignKey(
                'core.Farm',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='projectcost',
            name='farm',
            field=models.ForeignKey(
                'core.Farm',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True
            ),
        ),
    ]