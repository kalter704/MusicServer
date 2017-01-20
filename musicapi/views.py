# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from musicwebsite.models import PlayList, Song
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
		ensure_ascii = False
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
				ensure_ascii = False
				))
	return HttpResponse(json.dumps(
		{
			'response': {
				'error_code': 1
			}
		}))