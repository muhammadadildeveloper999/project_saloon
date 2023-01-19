# Generated by Django 4.1.3 on 2023-01-17 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0014_remove_portfolio_float_list_id_remove_review_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_name',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='saloon_id',
        ),
        migrations.RemoveField(
            model_name='saloon',
            name='service_id',
        ),
        migrations.RemoveField(
            model_name='service',
            name='description',
        ),
        migrations.RemoveField(
            model_name='service',
            name='image',
        ),
        migrations.RemoveField(
            model_name='service',
            name='price',
        ),
        migrations.RemoveField(
            model_name='service',
            name='service_type',
        ),
        migrations.RemoveField(
            model_name='services_list',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='category_id',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=0, upload_to='superadmin/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='service_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='category',
            name='service_type',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='saloon',
            name='category_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.category'),
        ),
        migrations.AddField(
            model_name='service',
            name='saloon_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.saloon'),
        ),
        migrations.AddField(
            model_name='services_list',
            name='service_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.service'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='service_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.service'),
        ),
    ]
