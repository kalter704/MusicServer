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
    url(r'^showallsongs/', views.show_all_songs, name = 'show_all_songs'),  

    url(r'^showfreeplaylists/', views.show_free_playlists, name = 'show_free_playlists'),
    url(r'^showfreeallsongs/', views.show_free_all_songs, name = 'show_free_all_songs'),
    url(r'^addfreeplaylist/', views.add_free_playlist, name = 'add_free_playlist'),
    url(r'^addfreesong/', views.add_free_song, name = 'add_free_song'),    
    url(r'^changefreeplaylist/(?P<playlist_id>[0-9]+)', views.change_free_playlist, name = 'change_free_playlist'),
    url(r'^changefreesong/(?P<song_id>[0-9]+)/', views.change_free_song, name = 'change_free_song'),
    url(r'^showfreesongs/(?P<playlist_id>[0-9]+)/', views.show_free_songs, name = 'show_free_songs'),
    
    url(r'^registration/', views.registration, name = 'registration'),
    url(r'^login/', views.log_in, name = 'log_in'),
    url(r'^logout/', views.log_out, name = 'log_out'),
    url(r'^showusers/', views.show_users, name = 'show_users'),
    url(r'^shownewusers/', views.show_new_users, name = 'show_new_users'),
    url(r'^addnewuser/(?P<newuser_id>[0-9]+)/', views.add_new_user, name = 'add_new_user'),
    url(r'^deletenewuser/(?P<newuser_id>[0-9]+)/', views.delete_new_user, name = 'delete_new_user'),
    url(r'^addsuperuser/(?P<user_id>[0-9]+)/', views.add_superuser, name = 'add_superuser'),
    url(r'^controlmobappversion/', views.control_mob_app_version, name = "control_mob_app_version"),

    url(r'^showads/', views.show_ads, name = 'show_ads'),
    url(r'^addad/', views.add_ad, name = 'add_ad'),
    url(r'^startad/(?P<ad_id>[0-9]+)/', views.start_ad, name = 'start_ad'),
    url(r'^stopad/(?P<ad_id>[0-9]+)/', views.stop_ad, name = 'stop_ad'),
    url(r'^delete_ad/(?P<ad_id>[0-9]+)/', views.delete_ad, name = 'delete_ad'),

    #url(r'^cleardatabase/', views.clear_database),

    #url(r'^getjson/', views.getSongs),
    #url(r'^play/', views.playSong),
]