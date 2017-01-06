# -*- coding: utf-8 -*-
import os
from MusicServer.settings import MEDIA_ROOT
from django.shortcuts import render
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from models import PlayList, Song

def index(request):
	return HttpResponse("Hello, world!!!")

def getSongs(request):
	playLists = PlayList.objects.all()
	json = '{<br>'
	for playList in playLists:
		for song in playList.song.all():
			json += 'PlaiList: ' + playList.title + ' ' + MEDIA_ROOT + '/' + str(song.song_file) + '<br>'
	json += '}'
	return HttpResponse(json)
	'''
	songs = Song.objects.all()
	json = '{<br>'
	for song in songs:
		json += str(song.song_file) + '<br>'
	json += '}'
	return HttpResponse(json)
	'''

def playSong(request):
    song = Song.objects.get(pk = 1)
    # song is an object which has a FileField name file
    filepath = os.path.join(MEDIA_ROOT, str(song.song_file))#.replace('\\', '/')
    wrapper = FileWrapper(file(filepath))
    response = HttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize(filepath)#.replace('/', '\\'))
    response['Content-Disposition'] = 'attachment; filename=%s' % str(song.song_file)
    #print(response)
    return response