# Generated by Django 5.0.2 on 2024-02-28 22:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URLShortener',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(max_length=250)),
                ('short_url_extension', models.CharField(max_length=15, unique=True)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
