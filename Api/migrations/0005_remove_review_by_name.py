# Generated by Django 4.1.3 on 2023-01-12 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0004_review_account_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='by_name',
        ),
    ]