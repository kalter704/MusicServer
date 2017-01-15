from django.contrib import admin

from .models import PlayList, Song, UdpatePlayList, NewUser

admin.site.register(PlayList)
admin.site.register(Song)
admin.site.register(UdpatePlayList)
admin.site.register(NewUser)