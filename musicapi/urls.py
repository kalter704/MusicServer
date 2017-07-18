from django.conf.urls import url

from views import getplaylists, getsongs, getinterstitialads, gettestjson, getbannerads
from views import getplaylists2, getsongs2

urlpatterns = [
    url(r'^getplaylists/', getplaylists, name = 'getplaylists'),
    url(r'^getsongs/', getsongs, name = 'getsongs'),
    url(r'^getinterstitialads/', getinterstitialads, name = 'getinterstitialads'),
    url(r'^getbannerads/', getbannerads, name = 'getbannerads'),
    url(r'^gettestjson/', gettestjson, name = 'gettestjson'),

    url(r'^v2/getplaylists/', getplaylists2, name = 'getplaylists2'),
    url(r'^v2/getsongs/', getsongs2, name = 'getsongs2'),
]