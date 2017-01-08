from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^addplaylist/', views.add_playlist, name = 'add_playlist'),
    url(r'^addsong/', views.add_song, name = 'add_song'),    
    url(r'^changeplaylist/(?P<playlist_id>[0-9]+)', views.change_playlist, name = 'change_playlist'),
    url(r'^changesong/(?P<song_id>[0-9]+)/', views.change_song, name = 'change_song'),
    url(r'^showplaylists/', views.show_playlists, name = 'show_playlists'),
    url(r'^showsongs/(?P<playlist_id>[0-9]+)/', views.show_songs, name = 'show_songs'),

    url(r'^cleardatabase/', views.clear_database),

    url(r'^getjson/', views.getSongs),
    url(r'^play/', views.playSong),
]