import json
from django.shortcuts import render
from django.http import HttpResponse
from musicwebsite.models import PlayList, Song, Ads, MobAppVersion, FreePlayList, FreeSong
from musicwebsite.func import isEmptyFields
from MusicServer.settings import MEDIA_URL

# Create your views here.

def getplaylists(request):
	playlists = PlayList.objects.all().order_by('pos')
	playlistArray = []
	count = 0
	for p in playlists:
		playlistArray.append({
			'id': p.id,
			'title': p.title,
			'school_owner': p.schoolOwner,
			'last_update': p.update_playlist.last_update,
			'pos': p.pos
			})
		count += 1
	return HttpResponse(json.dumps(
		{
			'response': {
				'count': count,
				'playlists': playlistArray
			}
		}, 
			ensure_ascii = True
		))

def getsongs(request):
	if request.GET:
		screen = request.GET.get('screen')
		if not isEmptyFields(screen):
			playlist_id = request.GET.get('playlist_id')
			song_id = request.GET.get('song_id')
			if not isEmptyFields(playlist_id):
				songs = Song.objects.filter(playList__id = playlist_id).order_by('pos')
			elif not isEmptyFields(song_id):
				songs = Song.objects.filter(pk = song_id)
			else:
				songs = Song.objects.all()
			songsArray = []
			count = 0
			for s in songs:
				img_url = MEDIA_URL + "album_img/" + str(s.id) + "_" + s.title + screen + "." + s.expansion
				song_url = MEDIA_URL + str(s.song_file)
				songsArray.append(
					{
						'id': s.id,
						'title': s.title,
						'singer': s.singer,
						'length': s.length,
						'pos': s.pos,
						'img_url': img_url,
						'song_url': song_url
					})
				count += 1
			return HttpResponse(json.dumps(
				{
					'response': {
						'count': count,
						'songs': songsArray
					}
				}, 
					ensure_ascii = True
				))
	return HttpResponse(json.dumps(
		{
			'response': {
				'error_code': 1
			}
		}, 
			ensure_ascii = True
		))

def getinterstitialads(request):
	ads = Ads.objects.filter(ad_type = 1).filter(state = 1)
	adsArray = []
	count = 0
	for ad in ads:
		ad_img = MEDIA_URL + str(ad.img)
		adsArray.append({
			'name': ad.name,
			'img': ad_img,
			'url': ad.url
			})
		count += 1
	return HttpResponse(json.dumps(
		{
			'count': count,
			'ads': adsArray
		}, 
			ensure_ascii = True
		))

def getbannerads(request):
	ads = Ads.objects.filter(ad_type = 2).filter(state = 1)
	adsArray = []
	count = 0
	for ad in ads:
		ad_img = MEDIA_URL + str(ad.img)
		adsArray.append({
			'name': ad.name,
			'img': ad_img,
			'url': ad.url
			})
		count += 1
	return HttpResponse(json.dumps(
		{
			'count': count,
			'ads': adsArray
		}, 
			ensure_ascii = True
		))

def gettestjson(request):
	return HttpResponse(json.dumps(
		{
			'response': {
				'count': "123",
				'ads': "adsArray"
			}
		}, 
			ensure_ascii = True
		))


def getplaylists2(request):
	if request.GET:
		os = request.GET.get('os')
		v = request.GET.get('v')
		if not isEmptyFields(os, v):
			a_versions = MobAppVersion.objects.all()
			if os == "ios":
				version = a_versions[0].ios_app
			else:
				version = a_versions[0].android_app
			if int(v) <= int(version):
				sounds = "main"
				playlists = PlayList.objects.all().order_by('pos')
			else:
				sounds = "free"
				playlists = FreePlayList.objects.all().order_by('pos')
			playlistArray = []
			count = 0
			for p in playlists:
				playlistArray.append({
					'id': p.id,
					'title': p.title,
					'school_owner': p.schoolOwner,
					'last_update': p.update_playlist.last_update,
					'pos': p.pos
					})
				count += 1
			return HttpResponse(json.dumps(
				{
					'response': {
						'sounds': sounds,
						'count': count,
						'playlists': playlistArray
					}
				}, 
					ensure_ascii = True
				))
	return HttpResponse(json.dumps(
		{
			'response': {
				'error_code': 1
			}
		}, 
			ensure_ascii = True
		))

def getsongs2(request):
	if request.GET:
		screen = request.GET.get('screen')
		sounds = request.GET.get('sounds')
		if not isEmptyFields(screen, sounds):
			playlist_id = request.GET.get('playlist_id')
			song_id = request.GET.get('song_id')
			if not isEmptyFields(playlist_id):
				if sounds == "main":
					songs = Song.objects.filter(playList__id = playlist_id).order_by('pos')
				else:
					songs = FreeSong.objects.filter(playList__id = playlist_id).order_by('pos')
			elif not isEmptyFields(song_id):
				if sounds == "main":
					songs = Song.objects.filter(pk = song_id)
				else:
					songs = FreeSong.objects.filter(pk = song_id)
			else:
				if sounds == "main":
					songs = Song.objects.all()
				else:
					songs = FreeSong.objects.all()
			songsArray = []
			count = 0
			if sounds == "main":
				folder = "album_img/"
			else:
				folder = "album_img/free_img/"
			for s in songs:
				img_url = MEDIA_URL + folder + str(s.id) + "_" + s.title + screen + "." + s.expansion
				song_url = MEDIA_URL + str(s.song_file)
				songsArray.append(
					{
						'id': s.id,
						'title': s.title,
						'singer': s.singer,
						'length': s.length,
						'pos': s.pos,
						'img_url': img_url,
						'song_url': song_url
					})
				count += 1
			return HttpResponse(json.dumps(
				{
					'response': {
						'sounds': sounds,
						'count': count,
						'songs': songsArray
					}
				}, 
					ensure_ascii = True
				))
	return HttpResponse(json.dumps(
		{
			'response': {
				'error_code': 1
			}
		}, 
			ensure_ascii = True
		))
