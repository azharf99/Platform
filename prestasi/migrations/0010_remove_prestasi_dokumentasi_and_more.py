# Generated by Django 4.1.3 on 2023-07-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestasi', '0009_dokumentasiprestasi_keterangan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestasi',
            name='dokumentasi',
        ),
        migrations.AlterField(
            model_name='prestasi',
            name='tahun_lomba',
            field=models.CharField(max_length=4),
        ),
    ]