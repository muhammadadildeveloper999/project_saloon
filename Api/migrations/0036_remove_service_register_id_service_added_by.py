# Generated by Django 4.1.3 on 2022-11-26 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0035_rename_facility_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='register_id',
        ),
        migrations.AddField(
            model_name='service',
            name='Added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.role'),
        ),
    ]
