# Generated by Django 5.1.7 on 2025-03-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_alter_property_google_map_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='vr_tour',
            field=models.FileField(blank=True, null=True, upload_to='vr_tours/'),
        ),
    ]
