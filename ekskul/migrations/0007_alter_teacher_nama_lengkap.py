# Generated by Django 4.1.3 on 2023-02-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekskul', '0006_alter_studentorganization_nama_siswa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='nama_lengkap',
            field=models.CharField(max_length=100, verbose_name='Nama Ustadz'),
        ),
    ]