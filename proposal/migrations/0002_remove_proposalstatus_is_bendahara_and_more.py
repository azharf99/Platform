# Generated by Django 4.1.3 on 2022-12-28 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ekskul', '0001_initial'),
        ('proposal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalstatus',
            name='is_bendahara',
        ),
        migrations.RemoveField(
            model_name='proposalstatus',
            name='is_kepsek',
        ),
        migrations.AddField(
            model_name='proposalstatus',
            name='alasan_wakasek',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='proposalstatus',
            name='foto_alasan',
            field=models.ImageField(blank=True, null=True, upload_to='proposal/koreksi'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='santri',
            field=models.ManyToManyField(blank=True, help_text='Pada PC/Laptop, tekan Ctrl untuk memilih banyak opsi', to='ekskul.studentorganization', verbose_name='Santri yang ikut'),
        ),
        migrations.AlterField(
            model_name='proposalstatus',
            name='is_wakasek',
            field=models.CharField(choices=[('Accepted', 'Diterima'), ('Rejected', 'Ditolak'), ('Pending', 'Menunggu respon'), ('Some Info Required', 'Kami membutuhkan informasi lebih detail')], default='Pending', max_length=100),
        ),
        migrations.CreateModel(
            name='ProposalStatusKepsek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_kepsek', models.CharField(choices=[('Accepted', 'Diterima'), ('Rejected', 'Ditolak'), ('Pending', 'Menunggu respon'), ('Some Info Required', 'Kami membutuhkan informasi lebih detail')], default='Pending', max_length=100)),
                ('alasan_kepsek', models.CharField(default='', max_length=200)),
                ('foto_alasan', models.ImageField(blank=True, null=True, upload_to='proposal/koreksi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.proposal')),
                ('status_wakasek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.proposalstatus')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalStatusBEndahara',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bendahara', models.CharField(choices=[('Accepted', 'Diterima'), ('Rejected', 'Ditolak'), ('Pending', 'Menunggu respon'), ('Some Info Required', 'Kami membutuhkan informasi lebih detail')], default='Pending', max_length=100)),
                ('alasan_bendahara', models.CharField(default='', max_length=200)),
                ('foto_alasan', models.ImageField(blank=True, null=True, upload_to='proposal/koreksi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.proposal')),
                ('status_kepsek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposal.proposalstatuskepsek')),
            ],
        ),
    ]