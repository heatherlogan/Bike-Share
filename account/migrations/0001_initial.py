# Generated by Django 2.2.5 on 2019-10-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('role', models.CharField(choices=[('0', 'Customer'), ('1', 'Operator'), ('2', 'Manager')], default='2', max_length=10)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('hires_in_progress', models.IntegerField(default=0)),
                ('current_location', models.CharField(default='', max_length=30)),
                ('wallet_balance', models.FloatField(default=0.0)),
                ('amount_owed', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
