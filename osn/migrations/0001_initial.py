# Generated by Django 4.1.3 on 2023-02-08 16:56

from django.db import migrations, models
import django.db.models.deletion
import ekskul.compress_image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ekskul', '0011_alter_extracurricular_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidangOSN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_bidang', models.CharField(max_length=50, verbose_name='Nama Bidang OSN')),
                ('jadwal_bimbingan', models.TextField(max_length=200)),
                ('slug', models.SlugField()),
                ('pembimbing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ekskul.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='SiswaOSN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidang_osn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osn.bidangosn')),
                ('nama_siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ekskul.student')),
            ],
        ),
        migrations.CreateModel(
            name='LaporanOSN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_pembinaan', models.DateField()),
                ('foto_bimbingan', ekskul.compress_image.CompressedImageField(default='no-image.png', help_text='Format foto harus .jpg atau .jpeg', quality=50, upload_to='ekskul/osn')),
                ('materi_pembinaan', models.TextField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bidang_osn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osn.bidangosn')),
                ('kehadiran_santri', models.ManyToManyField(to='osn.siswaosn')),
                ('pembimbing_osn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ekskul.teacher')),
            ],
        ),
    ]