# Generated by Django 4.1.3 on 2023-01-20 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0023_employee_name_employee_timing_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_name',
            name='employee_timing_id',
        ),
        migrations.AddField(
            model_name='employee_timing',
            name='employee_name_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.employee_name'),
        ),
    ]