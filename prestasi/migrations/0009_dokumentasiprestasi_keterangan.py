# Generated by Django 4.1.3 on 2023-07-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestasi', '0008_prestasi_kelas_peraih_prestasi'),
    ]

    operations = [
        migrations.AddField(
            model_name='dokumentasiprestasi',
            name='keterangan',
            field=models.TextField(blank=True, default='', max_length=300, null=True),
        ),
    ]