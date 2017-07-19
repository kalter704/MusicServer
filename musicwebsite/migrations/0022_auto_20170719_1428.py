# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicwebsite', '0021_freeplaylist_freesong_mobappversion_udpatefreeplaylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freesong',
            name='song_file',
            field=models.FileField(null=True, upload_to='songs/free_songs/'),
        ),
    ]
