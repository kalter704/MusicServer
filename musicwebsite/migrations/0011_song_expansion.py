# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0010_auto_20170109_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='expansion',
            field=models.CharField(default='jpg', max_length=5),
            preserve_default=False,
        ),
    ]