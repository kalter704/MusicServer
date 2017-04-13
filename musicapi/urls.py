from django.conf.urls import url

from views import getplaylists, getsongs, getinterstitialads, gettestjson, getbannerads

urlpatterns = [
    url(r'^getplaylists/', getplaylists, name = 'getplaylists'),
    url(r'^getsongs/', getsongs, name = 'getsongs'),
    url(r'^getinterstitialads/', getinterstitialads, name = 'getinterstitialads'),
    url(r'^getbannerads/', getbannerads, name = 'getbannerads'),
    url(r'^gettestjson/', gettestjson, name = 'gettestjson'),
]