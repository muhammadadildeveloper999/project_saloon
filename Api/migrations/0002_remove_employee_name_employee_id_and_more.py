# Generated by Django 4.1.3 on 2023-01-03 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
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
        migrations.DeleteModel(
            name='employee',
        ),
    ]
