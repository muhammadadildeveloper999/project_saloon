# Generated by Django 4.1.3 on 2022-11-19 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0004_register_lastname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='whitelistToken',
        ),
    ]