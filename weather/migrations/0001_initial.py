# Generated by Django 5.0 on 2024-11-06 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RequestHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('request_type', models.CharField(choices=[('web', 'Web'), ('telegram', 'Telegram')], max_length=10)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.city')),
            ],
            options={
                'ordering': ['-request_time'],
            },
        ),
        migrations.CreateModel(
            name='WeatherCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField()),
                ('pressure', models.IntegerField()),
                ('wind_speed', models.FloatField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.city')),
            ],
        ),
    ]
