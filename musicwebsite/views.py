# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

from models import PlayList, Song

def index(request):
	return HttpResponse("Hello, world!!!")

def getjson(request):
	playLists = PlayList.objects.all()
	json = '{<br>'
	for playList in playLists:
		for song in playList.song.all():
			json += 'PlaiList: ' + playList.title + ' ' + str(song.song_file) + '<br>'
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
