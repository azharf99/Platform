# Generated by Django 4.1.3 on 2022-12-21 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deskripsi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deskripsiekskul',
            name='color',
            field=models.CharField(default='primary', max_length=50),
        ),
        migrations.AddField(
            model_name='deskripsiekskul',
            name='url',
            field=models.CharField(default='data-detail', max_length=100),
        ),
        migrations.AddField(
            model_name='deskripsihome',
            name='color',
            field=models.CharField(default='primary', max_length=50),
        ),
        migrations.AddField(
            model_name='deskripsihome',
            name='url',
            field=models.CharField(default='not-available', max_length=100),
        ),
    ]
