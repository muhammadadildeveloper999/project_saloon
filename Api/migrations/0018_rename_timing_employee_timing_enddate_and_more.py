# Generated by Django 4.1.3 on 2023-01-18 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0017_remove_saloon_category_id_remove_service_saloon_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_timing',
            old_name='timing',
            new_name='enddate',
        ),
        migrations.RemoveField(
            model_name='service',
            name='description',
        ),
        migrations.RemoveField(
            model_name='service',
            name='price',
        ),
        migrations.RemoveField(
            model_name='service',
            name='service_type',
        ),
        migrations.AddField(
            model_name='employee_timing',
            name='startdate',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
