# Generated by Django 5.0.6 on 2024-07-04 09:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_drawing_image_drawing_base64_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagram',
            name='elements',
        ),
        migrations.AddField(
            model_name='diagram',
            name='base64_image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='diagram',
            name='edges',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name='diagram',
            name='nodes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), null=True, size=None),
        ),
    ]