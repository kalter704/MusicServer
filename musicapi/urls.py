from django.conf.urls import url

from views import getplaylists, getsongs

urlpatterns = [
    url(r'^getplaylists/', getplaylists, name = 'getplaylists'),
    url(r'^getsongs/', getsongs, name = 'getsongs'),
]