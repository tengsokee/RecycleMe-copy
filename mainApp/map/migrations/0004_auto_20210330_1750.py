# Generated by Django 3.1.6 on 2021-03-30 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_auto_20210329_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingpointphoto',
            name='photo_url',
            field=models.ImageField(upload_to='recyclingpoint_pics/'),
        ),
    ]
