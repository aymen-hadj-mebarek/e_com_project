# Generated by Django 4.2.5 on 2024-05-01 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]