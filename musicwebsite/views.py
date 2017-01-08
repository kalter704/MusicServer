# -*- coding: utf-8 -*-
import os
from MusicServer.settings import MEDIA_ROOT
from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from models import PlayList, Song, UdpatePlayList
from forms import FormPlayList, FormSong
from check_fields import isEmptyFields
from datetime import datetime
from work_with_img import save_img

def index(request):
	return render(request, 'index.html')

def show_playlists(request):
	playLists = PlayList.objects.all()
	return render(request, 'showPlayLists.html', { 'playLists': playLists })

def show_songs(request, playlist_id):
	songs = Song.objects.filter(playList__id = playlist_id)
	'''
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
	print(songs)
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
	'''
	return render(request, 'showSongs.html', { 'songs': songs })

def add_playlist(request):
	form = FormPlayList
	if request.POST:
		playList = request.POST.get('title')
		is_empty_field = isEmptyFields(playList)
		if is_empty_field:
			context = {
				'form': form,
				'is_empty_field': is_empty_field
			}
			return render(request, 'addPlayList.html', context)
		else:
			context = {
				'form': form,
				'add_successful': True
			}
			p = PlayList(title = playList)
			p.save()
			ud = UdpatePlayList(last_update = int(datetime.now().strftime("%y%m%d%H%M%S")), playList = p) 
			ud.save()
			return redirect('/addplaylist/')
	return render(request, 'addPlayList.html', { 'form': form })

def add_song(request):
	playLists = PlayList.objects.all()
	choices = [('', '')]
	for playList in playLists:
		choices.append([playList.title, playList.title])
	form = FormSong()
	form.fields['playList'].choices = choices
	if request.POST:
		title = request.POST.get('title')
		playList = request.POST.get('playList')
		songFile = request.POST.get('songFile')
		albumImg = request.POST.get('albumImg')
		if isEmptyFields(title, playList, songFile, albumImg):
			form = FormSong(initial = {'title': title, 'playList': playList})
			form.fields['playList'].choices = choices
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'addSong.html', context)
		else:
			save_img(title, request.FILES.get('albumImg'))
			context = {
				'form': form,
				'add_successful': True
			}
			#
			# Надо добавить логику сохранения!!!
			#
			return redirect('/addsong/')
	return render(request, 'addSong.html', { 'form': form })

def change_playlist(request, playlist_id):
	playList = PlayList.objects.get(pk = playlist_id)
	form = FormPlayList(initial={'title': playList.title})
	if request.POST:
		if request.POST.has_key('btn_save'):
			title = request.POST.get('title')
			#print("title = " + title)
			#print("isEmptyFields(title) = " + str(isEmptyFields(title)))
			if isEmptyFields(title):
				context = {
					'form': form,
					'is_empty_field': True,
					'playList': playList,
				}
				return render(request, 'changePlayList.html', context)
			else:
				playList.title = title
				playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				playList.save()
				playList.update_playlist.save()
				form = FormPlayList(initial={'title': playList.title})
				context = {
					'form': form,
					'add_successful': True,
					'playList': playList,
				}
				return render(request, 'changePlayList.html', context)
		elif request.POST.has_key('btn_delete'):
			playList.delete()
			return redirect('/showplaylists/')
	return render(request, 'changePlayList.html', { 'form': form, 'playList': playList })


def change_song(request, song_id):
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

def clear_database(request):
	'''
	playLists = PlayList.objects.all()
	for playList in playLists:
		playList.delete()
	songs = Song.objects.all()
	for song in songs:
		song.delete()
	return HttpResponse("Clear")
	'''
	return HttpResponse(MEDIA_ROOT)