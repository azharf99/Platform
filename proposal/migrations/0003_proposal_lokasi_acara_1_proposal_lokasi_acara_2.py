# Generated by Django 4.1.3 on 2022-12-28 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_remove_proposalstatus_is_bendahara_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='lokasi_acara_1',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='proposal',
            name='lokasi_acara_2',
            field=models.CharField(default='', max_length=200),
        ),
    ]
