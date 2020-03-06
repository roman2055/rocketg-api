# Generated by Django 2.2.7 on 2020-03-06 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0015_auto_20200226_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, max_length=50)),
                ('uid', models.CharField(blank=True, max_length=50)),
                ('client', models.CharField(blank=True, max_length=50)),
                ('data', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
