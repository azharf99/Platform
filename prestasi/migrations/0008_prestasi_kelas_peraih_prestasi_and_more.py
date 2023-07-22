# Generated by Django 4.1.3 on 2023-07-12 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestasi', '0007_alter_dokumentasiprestasi_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestasi',
            name='kelas_peraih_prestasi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dokumentasiprestasi',
            name='foto',
            field=models.FileField(blank=True, default='no-image.png', null=True, upload_to='prestasi'),
        ),
        migrations.AlterField(
            model_name='prestasi',
            name='sertifikat_1',
            field=models.FileField(blank=True, null=True, upload_to='prestasi/sertifikat'),
        ),
        migrations.AlterField(
            model_name='prestasi',
            name='sertifikat_2',
            field=models.FileField(blank=True, null=True, upload_to='prestasi/sertifikat'),
        ),
    ]