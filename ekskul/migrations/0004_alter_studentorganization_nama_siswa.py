# Generated by Django 4.1.3 on 2023-01-30 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekskul', '0003_remove_studentorganization_nama_siswa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentorganization',
            name='nama_siswa',
            field=models.ManyToManyField(help_text='Pada PC/Laptop, tekan Ctrl untuk memilih banyak opsi', to='ekskul.student'),
        ),
    ]