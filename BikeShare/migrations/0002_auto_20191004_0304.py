# Generated by Django 2.2.5 on 2019-10-04 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BikeShare', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faultybikes',
            options={'verbose_name_plural': 'Faulty Bikes'},
        ),
        migrations.AlterModelOptions(
            name='previousorders',
            options={'verbose_name_plural': 'Previous Orders'},
        ),
    ]
