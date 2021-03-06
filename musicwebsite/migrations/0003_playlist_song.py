# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-05 08:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('musicwebsite', '0002_auto_20170105_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('length', models.TimeField(null=True)),
                ('song_file', models.FileField(null=True, upload_to='songs/')),
                ('album_img', models.ImageField(null=True, upload_to='album_img/')),
                ('playList', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='musicwebsite.PlayList')),
            ],
        ),
    ]
