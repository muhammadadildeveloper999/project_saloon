# Generated by Django 4.1.3 on 2022-12-26 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0017_remove_category_saloon_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='multiple_category_slider',
            new_name='services_list',
        ),
    ]