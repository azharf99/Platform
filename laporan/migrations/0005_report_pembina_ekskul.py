# Generated by Django 4.1.3 on 2022-12-14 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ekskul', '0011_rename_ekskul_studentorganization_ekskul_siswa_and_more'),
        ('laporan', '0004_alter_uploadimage_foto_absensi'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='pembina_ekskul',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ekskul.teacher'),
        ),
    ]
