# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0008_auto_20170108_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='album_img_title',
        ),
        migrations.AlterField(
            model_name='song',
            name='length',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='song',
            name='pos',
            field=models.IntegerField(default=-1),
        ),
    ]