# Generated by Django 3.1 on 2020-09-06 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car_Days',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model', models.CharField(max_length=20)),
                ('Make', models.CharField(max_length=20)),
                ('Year', models.CharField(max_length=4)),
                ('Days_Online', models.FloatField()),
                ('Days_Online_1', models.FloatField()),
                ('Days_Online_2', models.FloatField()),
                ('Days_Online_3', models.FloatField()),
                ('Days_Online_4', models.FloatField()),
            ],
            options={
                'db_table': 'Car_Days',
                'managed': False,
            },
        ),
    ]
