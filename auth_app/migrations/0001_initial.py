# Generated by Django 5.0.4 on 2024-05-01 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('idcustomer', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('firstname', models.CharField(default='', max_length=50)),
                ('lastname', models.CharField(default='', max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('birthdate', models.DateField(default=datetime.date.today)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('phonenumber', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('picture', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
    ]
