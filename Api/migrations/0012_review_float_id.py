# Generated by Django 4.1.3 on 2023-01-13 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0011_review_saloon_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='float_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.float_list'),
        ),
    ]