# Generated by Django 2.1.5 on 2021-05-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='a',
            field=models.BooleanField(default='True'),
        ),
    ]
