# Generated by Django 2.2.5 on 2019-10-07 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeShare', '0006_auto_20191007_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='PreviousOrders',
        ),
    ]
