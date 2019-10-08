# Generated by Django 2.2.5 on 2019-10-07 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BikeShare', '0002_auto_20191004_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faultybikes',
            name='bike',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BikeShare.Bike'),
        ),
        migrations.AlterField(
            model_name='previousorders',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BikeShare.Order'),
        ),
    ]
