# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-06 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0013_auto_20170119_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='singer',
            field=models.CharField(default='', max_length=30),
        ),
    ]