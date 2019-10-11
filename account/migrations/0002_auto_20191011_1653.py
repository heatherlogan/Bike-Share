# Generated by Django 2.2.5 on 2019-10-11 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_customer',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_manager',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_operator',
        ),
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('0', 'Customer'), ('1', 'Operator'), ('2', 'Manager')], default='0', max_length=10),
        ),
    ]