# Generated by Django 4.1.3 on 2022-12-15 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laporan', '0007_remove_uploadimage_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='catatan_pembinaan',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
