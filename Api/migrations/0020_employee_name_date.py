# Generated by Django 4.1.3 on 2023-01-19 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0019_remove_employee_name_employee_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_name',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
