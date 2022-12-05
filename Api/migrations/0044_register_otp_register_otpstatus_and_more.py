# Generated by Django 4.1.3 on 2022-12-05 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0043_rename_facility_timing_service_service_timing'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='oTP',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='register',
            name='oTPStatus',
            field=models.CharField(default='False', max_length=255),
        ),
        migrations.AlterField(
            model_name='register',
            name='role_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Api.role'),
            preserve_default=False,
        ),
    ]
