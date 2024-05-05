# Generated by Django 5.0.3 on 2024-04-13 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=32, unique=True)),
                ('book_quantity', models.IntegerField(default=1)),
                ('book_fk_author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mangalib.author')),
            ],
        ),
    ]
