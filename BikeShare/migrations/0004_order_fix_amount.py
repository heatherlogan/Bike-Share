# Generated by Django 2.0.2 on 2019-10-24 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeShare', '0003_auto_20191018_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fix_amount',
            field=models.FloatField(default=0.0),
        ),
    ]