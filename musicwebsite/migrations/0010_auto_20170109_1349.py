# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0009_auto_20170109_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='pos',
            field=models.IntegerField(default=0),
        ),
    ]