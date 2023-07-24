# Generated by Django 4.0.6 on 2023-07-22 15:21

from django.db import migrations, models
import ekskul.compress_image


class Migration(migrations.Migration):

    dependencies = [
        ('ekskul', '0004_alter_extracurricular_logo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extracurricular',
            old_name='nama',
            new_name='nama_ekskul',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='nama',
            new_name='nama_siswa',
        ),
        migrations.RenameField(
            model_name='studentorganization',
            old_name='ekskul_siswa',
            new_name='ekskul',
        ),
        migrations.RenameField(
            model_name='studentorganization',
            old_name='nama_siswa',
            new_name='siswa',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='nama_lengkap',
            new_name='nama_pembina',
        ),
        migrations.RemoveField(
            model_name='extracurricular',
            name='jadwal_tambahan',
        ),
        migrations.RemoveField(
            model_name='extracurricular',
            name='waktu_tambahan',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='gelar_belakang',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='gelar_depan',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='jabatan_khusus',
        ),
        migrations.AddField(
            model_name='extracurricular',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='alamat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='foto',
            field=ekskul.compress_image.CompressedImageField(blank=True, default='blank-profile.png', help_text='Format foto .jpg/.jpeg', null=True, quality=50, upload_to='student'),
        ),
        migrations.AddField(
            model_name='student',
            name='jenis_kelamin',
            field=models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], default='L', max_length=10),
        ),
        migrations.AddField(
            model_name='student',
            name='nomor_hp',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, default='Aktif', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='tanggal_lahir',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='tempat_lahir',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='alamat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='jenis_kelamin',
            field=models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], default='L', max_length=1),
        ),
        migrations.AlterField(
            model_name='extracurricular',
            name='logo',
            field=ekskul.compress_image.CompressedImageField(blank=True, default='no-image.png', help_text='format logo .jpg/.jpeg', null=True, quality=50, upload_to='ekskul/logo'),
        ),
        migrations.AlterField(
            model_name='student',
            name='nis',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='nisn',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, default='smaitalbinaa.ekskul@outlook.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='foto',
            field=ekskul.compress_image.CompressedImageField(blank=True, default='blank-profile.png', help_text='format foto .jpg/.jpeg', null=True, quality=50, upload_to='user'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='no_hp',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]