# Generated by Django 4.2b1 on 2023-03-07 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poi',
            fields=[
                ('poi_id', models.AutoField(help_text='auto increment PK', primary_key=True, serialize=False)),
                ('latitude', models.FloatField(blank=True, help_text='위도', null=True)),
                ('longitude', models.FloatField(blank=True, help_text='경도', null=True)),
                ('altitude', models.FloatField(blank=True, help_text='고도', null=True)),
            ],
            options={
                'db_table': 'poi',
                'managed': False,
            },
        ),
    ]
