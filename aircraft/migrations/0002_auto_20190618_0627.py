# Generated by Django 2.2.2 on 2019-06-18 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aircraft', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraftpage',
            name='billing_last_updated',
            field=models.DateField(blank=True, null=True),
        ),
    ]
