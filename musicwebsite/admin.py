from django.contrib import admin

from .models import PlayList, Song, UdpatePlayList

admin.site.register(PlayList)
admin.site.register(Song)
admin.site.register(UdpatePlayList)
