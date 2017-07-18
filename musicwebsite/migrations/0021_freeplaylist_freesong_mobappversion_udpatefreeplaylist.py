# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0020_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreePlayList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('pos', models.IntegerField(default=0)),
                ('schoolOwner', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FreeSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('length', models.IntegerField(default=-1)),
                ('song_file', models.FileField(null=True, upload_to='songs/')),
                ('pos', models.IntegerField(default=0)),
                ('expansion', models.CharField(max_length=5)),
                ('singer', models.CharField(default='', max_length=50)),
                ('playList', models.ForeignKey(related_name='songs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='musicwebsite.FreePlayList', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MobAppVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('android_app', models.IntegerField(default=-1)),
                ('ios_app', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='UdpateFreePlayList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_update', models.BigIntegerField()),
                ('playList', models.OneToOneField(related_name='update_playlist', to='musicwebsite.FreePlayList')),
            ],
        ),
    ]
