from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^addalbum/', views.add_album, name = 'add_album'),
    url(r'^addsong/', views.add_song, name = 'add_song'),
    url(r'^showalbums/', views.show_albums, name = 'show_albums'),
    url(r'^showsongs/(?P<album_id>[0-9]+)/', views.show_songs, name = 'show_songs'),

    url(r'^getjson/', views.getSongs),
    url(r'^play/', views.playSong),
]