# Generated by Django 2.2.5 on 2019-10-17 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeShare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='station_latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='station_longitude',
            field=models.FloatField(null=True),
        ),
    ]