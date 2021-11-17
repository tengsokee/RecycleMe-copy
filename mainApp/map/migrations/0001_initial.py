# Generated by Django 3.1.6 on 2021-03-29 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecyclingPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('categories', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('postalCode', models.CharField(max_length=6)),
                ('description', models.TextField(max_length=500)),
                ('hyperlink', models.URLField(max_length=300)),
                ('latitude', models.CharField(default='', max_length=50)),
                ('longitude', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RecyclingPointPhotoToVet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('photo_url', models.ImageField(max_length=300, upload_to='')),
                ('photo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.recyclingpoint')),
            ],
        ),
        migrations.CreateModel(
            name='RecyclingPointPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('photo_url', models.ImageField(upload_to='recyclingpoint_pics/')),
                ('photo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.recyclingpoint')),
            ],
        ),
    ]
