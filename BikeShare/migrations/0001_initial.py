# Generated by Django 2.0.2 on 2019-09-30 22:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bikeid', models.CharField(max_length=10)),
                ('current_usage', models.CharField(choices=[('U', 'In Use'), ('N', 'Not In Use')], max_length=1)),
                ('condition', models.CharField(choices=[('O', 'Ok'), ('F', 'Faulty')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('wallet_balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=10)),
                ('check_in_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('bikeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeShare.Bike')),
                ('customerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BikeShare.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stationid', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='bike',
            name='stationid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BikeShare.Station'),
        ),
    ]
