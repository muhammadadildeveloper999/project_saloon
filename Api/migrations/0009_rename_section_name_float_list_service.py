# Generated by Django 4.1.3 on 2022-12-21 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0008_remove_service_section_id_float_list_category_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='float_list',
            old_name='section_name',
            new_name='service',
        ),
    ]
