# Generated by Django 5.0.3 on 2024-05-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_customer_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='picture',
            field=models.ImageField(blank=True, default='user.png', upload_to=''),
        ),
    ]
