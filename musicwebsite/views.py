# -*- coding: utf-8 -*-
import os
import time
from MusicServer.settings import MEDIA_ROOT
from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from models import PlayList, Song, UdpatePlayList
from forms import FormPlayList, FormSong
from func import isEmptyFields, removeBlankSpaceInList, insertSongToPos, saveImg, renameImg, deleteImg
from datetime import datetime
from mutagen.mp3 import MP3


def index(request):
	return render(request, 'index.html')

def show_playlists(request):
	playLists = PlayList.objects.all()
	return render(request, 'showPlayLists.html', { 'playLists': playLists })

def show_songs(request, playlist_id):
	#print("qwqqqqqqqqqqqqqq")
	songs = Song.objects.filter(playList__id = playlist_id).order_by('pos')
	'''
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
	print(songs)
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
	'''
	return render(request, 'showSongs.html', { 'songs': songs, 'playList': PlayList.objects.get(pk = playlist_id).title })

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
		songFile = request.FILES.get('songFile')
		albumImg = request.FILES.get('albumImg')
		print(title)
		print(playList)
		#print("songFile = " + str(songFile))
		print(str(albumImg))
		print(albumImg)
		if isEmptyFields(title, playList, songFile, albumImg):
			form = FormSong(initial = {'title': title, 'playList': playList})
			form.fields['playList'].choices = choices
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'addSong.html', context)
		else:
			### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			playListObj = PlayList.objects.get(title = playList)
			songObj = Song(title = title, song_file = request.FILES.get('songFile'))
			songObj.playList = playListObj
			img_name = albumImg.name
			if img_name.endswith(".jpg"):
				songObj.expansion = "jpg"
			elif img_name.endswith(".jpeg"):
				songObj.expansion = "jpeg"
			elif img_name.endswith(".png"):
				songObj.expansion = "png"

			songObj.save()
			playListObj.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
			playListObj.update_playlist.save()
			#print("song_file = " + str(songObj.song_file))
			#print("albumImg = " + str(albumImg.name))
			saveImg(songObj.id, title, albumImg.name, albumImg)
			audio = MP3(MEDIA_ROOT + "/" + str(songObj.song_file))
			#print("audio length = " + str(audio.info.length))
			songObj.length = int(round(audio.info.length))
			ssss = Song.objects.filter(playList = playListObj).order_by("-pos")[:1]
			songObj.pos = ssss[0].pos + 1
			songObj.save()
			context = {
				'form': form,
				'add_successful': True
			}
			return redirect('/addsong/')
	return render(request, 'addSong.html', { 'form': form })

def change_playlist(request, playlist_id):
	playList = PlayList.objects.get(pk = playlist_id)
	form = FormPlayList(initial={'title': playList.title})
	if request.POST:
		#print("request.POST")
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
	song = Song.objects.get(pk = song_id)
	playLists = PlayList.objects.all()
	choices = [('', '')]
	for playList in playLists:
		choices.append([playList.title, playList.title])
	form = FormSong(initial={'title': song.title, 'pos': song.pos})
	form.fields['playList'].choices = choices
	if request.POST:
		####---------------------
		if request.POST.has_key('btn_save'):
			title = request.POST.get('title')
			pos = request.POST.get('pos')
			playListTitle = request.POST.get('playList')
			songFile = request.FILES.get('songFile')
			albumImg = request.FILES.get('albumImg')
			#print(songFile)
			if isEmptyFields(title, pos, playListTitle):
				context = {
					'form': form,
					'is_empty_field': True,
					'song': song,
				}
				return render(request, 'changeSong.html', context)
			else:
				if not isEmptyFields(songFile):
					os.remove(MEDIA_ROOT + '/' + str(song.song_file))
					#print("path: " + MEDIA_ROOT + '/' + str(song.song_file))
					song.song_file = songFile
					#audio = MP3(songFile)
					#time.sleep(5)
					#audio = MP3(MEDIA_ROOT + "/" + str(song.song_file))
					#song.length = int(round(audio.info.length))
				if song.playList.title != playListTitle:
					#old_pos = song.pos
					#print("song.pos = " + str(song.pos))
					#print("song.playList.id = " + str(song.playList.id))
					removeBlankSpaceInList(song.pos, song.playList.id)
					p = PlayList.objects.get(title = playListTitle)
					song.playList = p
					ssss = Song.objects.filter(playList = p).order_by("-pos")[:1]
					print(ssss)
					if len(ssss) != 0:
						song.pos = ssss[0].pos + 1
					else:
						song.pos = 1
				elif song.pos != pos:
					insertSongToPos(song, int(pos))

				if song.title != title:
					renameImg(song.id, song.title, title, song.expansion)
					song.title = title
				if not isEmptyFields(albumImg):
					#deleteImg(song.id, song.title, albumImg.name)
					if albumImg.name.endswith(".jpg"):
						expansion_temp = "jpg"
					elif albumImg.name.endswith(".jpeg"):
						expansion_temp = "jpeg"
					elif albumImg.name.endswith(".png"):
						expansion_temp = "png"
					if song.expansion != expansion_temp:
						deleteImg(song.id, song.title, song.expansion)
						song.expansion = expansion_temp
					saveImg(song.id, song.title, albumImg.name, albumImg)
				if not isEmptyFields(songFile):
					audio = MP3(MEDIA_ROOT + "/" + str(song.song_file))
					song.length = int(round(audio.info.length))
				#playList.title = title
				#playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				#playList.save()
				#playList.update_playlist.save()
				#form = FormPlayList(initial={'title': playList.title})
				song.save()
				song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				song.playList.update_playlist.save()
				form = FormSong(initial={'title': song.title, 'pos': song.pos})
				form.fields['playList'].choices = choices
				context = {
					'form': form,
					'add_successful': True,
					'song': song
				}
				return render(request, 'changeSong.html', context)
		elif request.POST.has_key('btn_delete'):
			#playList.delete()
			song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
			song.playList.update_playlist.save()
			deleteImg(song.id, song.title, song.expansion)
			path = os.path.join(MEDIA_ROOT, str(song.song_file))
			removeBlankSpaceInList(song.pos, song.playList.id)
			#print("path: " + str(path))
			os.remove(path)
			song.delete()
			return redirect('/showsongs/' + str(song.playList.id) + '/')
		elif request.POST.has_key('btn_back'):
			print("btn_back")
			return redirect('/showsongs/' + str(song.playList.id) + '/')
		####---------------------
	return render(request, 'changeSong.html', { 'form': form, 'song': song })

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
    song = Song.objects.all()[0]
    # song is an object which has a FileField name file
    filepath = os.path.join(MEDIA_ROOT, str(song.song_file))#.replace('\\', '/')
    wrapper = FileWrapper(file(filepath))
    response = HttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize(filepath)#.replace('/', '\\'))
    response['Content-Disposition'] = 'attachment; filename=%s' % str(song.song_file)
    #print(response)
    return response

def clear_database(request):
	playLists = PlayList.objects.all()
	for playList in playLists:
		playList.delete()
	songs = Song.objects.all()
	for song in songs:
		song.delete()
	return HttpResponse("Clear")	
	#return HttpResponse(MEDIA_ROOT)