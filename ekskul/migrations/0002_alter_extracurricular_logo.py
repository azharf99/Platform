# Generated by Django 4.1.3 on 2022-12-31 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekskul', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extracurricular',
            name='logo',
            field=models.ImageField(blank=True, default='no-image.png', null=True, upload_to='ekskul/logo'),
        ),
    ]
