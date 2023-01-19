# Generated by Django 4.1.3 on 2023-01-19 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0018_rename_timing_employee_timing_enddate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_name',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='employee_timing',
            name='employee_id',
        ),
        migrations.AddField(
            model_name='employee_name',
            name='saloon_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.saloon'),
        ),
        migrations.AddField(
            model_name='employee_timing',
            name='saloon_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.saloon'),
        ),
    ]
