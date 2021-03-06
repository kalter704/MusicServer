# -*- coding: utf-8 -*-
import os
import time
from MusicServer.settings import MEDIA_ROOT
from django.shortcuts import render, redirect
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from models import PlayList, Song, UdpatePlayList, NewUser, Ads, UserType, FreePlayList, FreeSong, UdpateFreePlayList, MobAppVersion
from forms import FormPlayList, FormSong, FormRegisterUser, FormLogInUser, FormSortBy, FormAd, FormMobAppVersion
from func import isEmptyFields, removeBlankSpaceInList, insertSongToPos, saveImg, renameImg, deleteImg, isExistUser, insertPlaylistToPos, insertFreePlaylistToPos, insertFreeSongToPos, removeBlankSpaceInFreeList, saveFreeImg, renameFreeImg, deleteFreeImg
from datetime import datetime
from mutagen.mp3 import MP3
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
	return render(request, 'index.html')

@login_required
def show_playlists(request):
	playLists = PlayList.objects.all().order_by('pos')
	return render(request, 'showPlayLists.html', { 'playLists': playLists })

@login_required
def show_songs(request, playlist_id):
	songs = Song.objects.filter(playList__id = playlist_id).order_by('pos')
	return render(request, 'showSongs.html', { 'songs': songs, 'playList': PlayList.objects.get(pk = playlist_id).title })

@login_required
def show_all_songs(request):
	form = FormSortBy(initial = {'objSort': 'Названию', 'ubVozr': 'Возрастанию'})
	form.fields['objSort'].choices = [
		('Названию','Названиию'), 
		('Исполнителю', 'Исполнителю'),
		('Плейлисту', 'Плейлисту'),
		('Длине', 'Длине')
	] 
	form.fields['ubVozr'].choices = [
		('Возр','Возр'), 
		('Убыв', 'Убыв')
	]
	sortBy = "title"
	direction = ""
	if request.POST:
		#print("request == true")
		objSortBy = request.POST.get("objSort")
		ubVozr = request.POST.get("ubVozr")
		#print("objSortBy = " + objSortBy)
		if objSortBy == u"Названию":
			#print("sortBy = title")
			sortBy = "title"
		elif objSortBy == u"Исполнителю":
			sortBy = "singer"
		elif objSortBy == u"Плейлисту":
			#print("sortBy = playList__title")
			sortBy = "playList__title"
		elif objSortBy == u"Длине":
			#print("sortBy = length")
			sortBy = "length"
		if ubVozr == u"Возр":
			direction = ""
		if ubVozr == u"Убыв":
			direction = "-"
		form = FormSortBy(initial = {'objSort': objSortBy, 'ubVozr': ubVozr})
		form.fields['objSort'].choices = [
			('Названию','Названиию'), 
			('Исполнителю', 'Исполнителю'),
			('Плейлисту', 'Плейлисту'),
			('Длине', 'Длине')
		] 
		form.fields['ubVozr'].choices = [
			('Возр','Возр'), 
			('Убыв', 'Убыв')
		]
	#print("direction + sortBy = " + direction + sortBy)
	songs = Song.objects.all().order_by(direction + sortBy)
	return render(request, 'showAllSongs.html', { 'form': form, 'songs': songs })

@login_required
def add_playlist(request):
	form = FormPlayList
	if request.POST:
		playList = request.POST.get('title')
		schoolOwner = request.POST.get('schoolOwner')
		is_empty_field = isEmptyFields(playList, schoolOwner)
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
			lastPlayList = PlayList.objects.all().order_by('-pos')[:1]
			if len(lastPlayList) != 0:
				tempPos = lastPlayList[0].pos + 1
			else:
				tempPos = 1
			p = PlayList(title = playList, schoolOwner = schoolOwner, pos = tempPos)
			p.save()
			ud = UdpatePlayList(last_update = int(datetime.now().strftime("%y%m%d%H%M%S")), playList = p) 
			ud.save()
			return redirect('/addplaylist/')
	return render(request, 'addPlayList.html', { 'form': form })

@login_required
def add_song(request):
	playLists = PlayList.objects.all()
	choices = [('', '')]
	for playList in playLists:
		choices.append([playList.title, playList.title])
	form = FormSong()
	form.fields['playList'].choices = choices
	if request.POST:
		title = request.POST.get('title')
		singer = request.POST.get('singer')
		playList = request.POST.get('playList')
		songFile = request.FILES.get('songFile')
		albumImg = request.FILES.get('albumImg')
		print(title)
		print(singer)
		print(playList)
		#print("songFile = " + str(songFile))
		print(str(albumImg))
		print(albumImg)
		if isEmptyFields(title, singer, playList, songFile, albumImg):
			form = FormSong(initial = {'title': title, 'playList': playList, 'singer': singer})
			form.fields['playList'].choices = choices
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'addSong.html', context)
		else:
			### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			playListObj = PlayList.objects.get(title = playList)
			songObj = Song(title = title, singer = singer, song_file = request.FILES.get('songFile'))
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

@login_required
def change_playlist(request, playlist_id):
	playList = PlayList.objects.get(pk = playlist_id)
	form = FormPlayList(initial={'title': playList.title, 'schoolOwner': playList.schoolOwner, 'pos': playList.pos})
	if request.POST:
		#print("request.POST")
		if request.POST.has_key('btn_save'):
			title = request.POST.get('title')
			schoolOwner = request.POST.get('schoolOwner')
			pos = request.POST.get('pos')
			#print("title = " + title)
			#print("isEmptyFields(title) = " + str(isEmptyFields(title)))
			if isEmptyFields(title, schoolOwner, pos):
				context = {
					'form': form,
					'is_empty_field': True,
					'playList': playList,
				}
				return render(request, 'changePlayList.html', context)
			else:
				playList.title = title
				playList.schoolOwner = schoolOwner
				#####!!!!!!!!!!!!!!!!!! Position
				if int(pos) != playList.pos:
					insertPlaylistToPos(playList, int(pos))
				playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				playList.save()
				playList.update_playlist.save()
				form = FormPlayList(initial={'title': playList.title, 'schoolOwner': playList.schoolOwner, 'pos': playList.pos})
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

@login_required
def change_song(request, song_id):
	song = Song.objects.get(pk = song_id)
	playLists = PlayList.objects.all()
	choices = [('', '')]
	for playList in playLists:
		choices.append([playList.title, playList.title])
	form = FormSong(initial={'title': song.title, 'pos': song.pos, 'singer': song.singer})
	form.fields['playList'].choices = choices 
	if request.POST:
		if request.POST.has_key('btn_save'):
			title = request.POST.get('title')
			singer = request.POST.get('singer')
			pos = request.POST.get('pos')
			playListTitle = request.POST.get('playList')
			songFile = request.FILES.get('songFile')
			albumImg = request.FILES.get('albumImg')
			#print(songFile)
			if isEmptyFields(title, singer, pos, playListTitle):
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
					song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
					song.playList.update_playlist.save()
					p = PlayList.objects.get(title = playListTitle)
					song.playList = p
					ssss = Song.objects.filter(playList = p).order_by("-pos")[:1]
					#print(ssss)
					if len(ssss) != 0:
						song.pos = ssss[0].pos + 1
					else:
						song.pos = 1
				elif song.pos != int(pos):
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
					song.save()
					audio = MP3(MEDIA_ROOT + "/" + str(song.song_file))
					song.length = int(round(audio.info.length))
				if song.singer != singer:
					song.singer = singer
				#playList.title = title
				#playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				#playList.save()
				#playList.update_playlist.save()
				#form = FormPlayList(initial={'title': playList.title})
				song.save()
				song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				song.playList.update_playlist.save()
				form = FormSong(initial={'title': song.title, 'pos': song.pos, 'singer': song.singer})
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
	return render(request, 'changeSong.html', { 'form': form, 'song': song })

def registration(request):
	form = FormRegisterUser
	if request.POST:
		login = request.POST.get("login")
		password = request.POST.get("password")
		password2 = request.POST.get("password2")
		if isEmptyFields(login, password, password2):
			form = FormRegisterUser(initial={'login': login})
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'registration.html', context)
		elif password != password2:
			form = FormRegisterUser(initial={'login': login})
			context = {
				'form': form,
				'is_not_match_pass': True,
			}
			return render(request, 'registration.html', context)
		elif isExistUser(login):
			form = FormRegisterUser(initial={'login': login})
			context = {
				'form': form,
				'is_user_exist': True,
			}
			return render(request, 'registration.html', context)
		else:
			newUser = NewUser(name = login, password = password)
			newUser.save()
			context = {
				'form': form,
				'is_successfull': True,
			}
			return render(request, 'registration.html', context)
	return render(request, 'registration.html', { 'form': form })

def log_in(request):
	form = FormLogInUser
	if request.POST:
		login = request.POST.get("login")
		password = request.POST.get("password")
		if isEmptyFields(login, password):
			form = FormRegisterUser(initial={'login': login})
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'logIn.html', context)
		else:
			user = auth.authenticate(username = login, password = password)
			if user is not None:
				auth.login(request, user)
				next_page = request.POST.get('next_page')
				print(next_page)
				if (next_page == None or next_page == ''):
					return redirect('/')
				else:
					return redirect(next_page)
			else:
				form = FormRegisterUser(initial={'login': login})
				context = {
					'form': form,
					'is_error_user': True,
				}
				return render(request, 'logIn.html', context)
	return render(request, 'logIn.html', { 'form': form })

def log_out(request):
	auth.logout(request)
	return redirect('/')

@login_required
def show_users(request):
	users = User.objects.all()
	return render(request, 'showUsers.html', { 'users': users })

@login_required
def add_superuser(request, user_id):
	user = User.objects.get(pk = user_id)
	user.user_type.type = 1
	user.user_type.save()
	users = User.objects.all()
	return render(request, 'showUsers.html', { 'users': users })

@login_required
def show_new_users(request):
	newUsers = NewUser.objects.all()
	return render(request, 'showNewUsers.html', { 'newUsers': newUsers })

@login_required
def add_new_user(request, newuser_id):
	try:
		newUser = NewUser.objects.get(pk = newuser_id)
		user = User.objects.create_user(username = newUser.name, password = newUser.password)
		user.save()
		userType = UserType(user = user, type = 0)
		userType.save()
		newUser.delete()
	except:
		print('Except')
	return redirect('/shownewusers/')

@login_required
def delete_new_user(request, newuser_id):
	try:
		newUser = NewUser.objects.get(pk = newuser_id)
		newUser.delete()
	except:
		print('Except')
	return redirect('/shownewusers/')

'''
def getSongs(request):
	playLists = PlayList.objects.all()
	json = '{<br>'
	for playList in playLists:
		for song in playList.song.all():
			json += 'PlaiList: ' + playList.title + ' ' + MEDIA_ROOT + '/' + str(song.song_file) + '<br>'
	json += '}'
	return HttpResponse(json)
	# разделитель 
	songs = Song.objects.all()
	json = '{<br>'
	for song in songs:
		json += str(song.song_file) + '<br>'
	json += '}'
	return HttpResponse(json)
'''

'''
def playSong(request):
    song = Song.objects.all()[0]
    filepath = os.path.join(MEDIA_ROOT, str(song.song_file))
    wrapper = FileWrapper(file(filepath))
    response = HttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = 'attachment; filename=%s' % str(song.song_file)
    return response
'''

@login_required
def start_ad(request, ad_id):
	try:
		ad = Ads.objects.get(pk = ad_id)
		ad.state = 1
		ad.save()
	except Exception as e:
		print("start_ad ERROR")
	return show_ads(request)

@login_required
def stop_ad(request, ad_id):
	try:
		ad = Ads.objects.get(pk = ad_id)
		ad.state = 2
		ad.save()
	except Exception as e:
		print("stop_ad ERROR")
	return show_ads(request)

@login_required
def	delete_ad(request, ad_id):
	try:
		ad = Ads.objects.get(pk = ad_id)
		path = os.path.join(MEDIA_ROOT, str(ad.img))
		os.remove(path)
		ad.delete()
	except Exception as e:
		print("delete_ad ERROR")
	return show_ads(request)

@login_required
def show_ads(request):
	ads = Ads.objects.all()
	return render(request, 'showAds.html', { 'ads': ads });

@login_required
def add_ad(request):
	form = FormAd
	if request.POST:
		title = request.POST.get('title')
		ad_type = request.POST.get('ad_type')
		img = request.FILES.get('img')
		url = request.POST.get('url')
		if isEmptyFields(title, ad_type, img, url):
			form = FormAd(initial = {'title': title, 'ad_type': ad_type, 'url': url})
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'addAd.html', context)
		else:
			### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			newAd = Ads(name = title, img = img, state = 1, ad_type = ad_type, url = url)
			newAd.save()
			context = {
				'form': form,
				'add_successful': True
			}
			return render(request, 'addAd.html', context)
	return render(request, 'addAd.html', { 'form': form });

@login_required
def control_mob_app_version(request):
	versions = MobAppVersion.objects.all()
	if len(versions) == 0:
		versions = [ MobAppVersion(android_app = 0, ios_app = 0) ]
		versions[0].save()
	form = FormMobAppVersion
	if request.POST:
		android_version = request.POST.get('androidVersion')
		ios_version = request.POST.get('iosVersion')
		if isEmptyFields(android_version) == False:
			android_version_i = int(android_version)
			versions[0].android_app = android_version_i
		if isEmptyFields(ios_version) == False:
			ios_version_i = int(ios_version)
			versions[0].ios_app = ios_version_i
		versions[0].save()
		return redirect('/controlmobappversion/')
	return render(request, 'controlMobAppVersion.html', { 'form': form, 'versions': versions[0] })

@login_required
def show_free_playlists(request):
	playLists = FreePlayList.objects.all().order_by('pos')
	return render(request, 'showFreePlayLists.html', { 'playLists': playLists })

@login_required
def add_free_playlist(request):
	form = FormPlayList
	if request.POST:
		playList = request.POST.get('title')
		schoolOwner = request.POST.get('schoolOwner')
		is_empty_field = isEmptyFields(playList, schoolOwner)
		if is_empty_field:
			context = {
				'form': form,
				'is_empty_field': is_empty_field
			}
			return render(request, 'addFreePlayList.html', context)
		else:
			context = {
				'form': form,
				'add_successful': True
			}
			lastPlayList = FreePlayList.objects.all().order_by('-pos')[:1]
			if len(lastPlayList) != 0:
				tempPos = lastPlayList[0].pos + 1
			else:
				tempPos = 1
			p = FreePlayList(title = playList, schoolOwner = schoolOwner, pos = tempPos)
			p.save()
			ud = UdpateFreePlayList(last_update = int(datetime.now().strftime("%y%m%d%H%M%S")), playList = p) 
			ud.save()
			return redirect('/addfreeplaylist/')
	return render(request, 'addFreePlayList.html', { 'form': form })

@login_required
def change_free_playlist(request, playlist_id):
	playList = FreePlayList.objects.get(pk = playlist_id)
	form = FormPlayList(initial={'title': playList.title, 'schoolOwner': playList.schoolOwner, 'pos': playList.pos})
	if request.POST:
		#print("request.POST")
		if request.POST.has_key('btn_save'):
			title = request.POST.get('title')
			schoolOwner = request.POST.get('schoolOwner')
			pos = request.POST.get('pos')
			#print("title = " + title)
			#print("isEmptyFields(title) = " + str(isEmptyFields(title)))
			if isEmptyFields(title, schoolOwner, pos):
				context = {
					'form': form,
					'is_empty_field': True,
					'playList': playList,
				}
				return render(request, 'changeFreePlayList.html', context)
			else:
				playList.title = title
				playList.schoolOwner = schoolOwner
				#####!!!!!!!!!!!!!!!!!! Position
				if int(pos) != playList.pos:
					insertFreePlaylistToPos(playList, int(pos))
				playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				playList.save()
				playList.update_playlist.save()
				form = FormPlayList(initial={'title': playList.title, 'schoolOwner': playList.schoolOwner, 'pos': playList.pos})
				context = {
					'form': form,
					'add_successful': True,
					'playList': playList,
				}
				return render(request, 'changeFreePlayList.html', context)
		elif request.POST.has_key('btn_delete'):
			playList.delete()
			return redirect('/showfreeplaylists/')
	return render(request, 'changeFreePlayList.html', { 'form': form, 'playList': playList })


@login_required
def show_free_all_songs(request):
	form = FormSortBy(initial = {'objSort': 'Названию', 'ubVozr': 'Возрастанию'})
	form.fields['objSort'].choices = [
		('Названию','Названиию'), 
		('Исполнителю', 'Исполнителю'),
		('Плейлисту', 'Плейлисту'),
		('Длине', 'Длине')
	] 
	form.fields['ubVozr'].choices = [
		('Возр','Возр'), 
		('Убыв', 'Убыв')
	]
	sortBy = "title"
	direction = ""
	if request.POST:
		#print("request == true")
		objSortBy = request.POST.get("objSort")
		ubVozr = request.POST.get("ubVozr")
		#print("objSortBy = " + objSortBy)
		if objSortBy == u"Названию":
			#print("sortBy = title")
			sortBy = "title"
		elif objSortBy == u"Исполнителю":
			sortBy = "singer"
		elif objSortBy == u"Плейлисту":
			#print("sortBy = playList__title")
			sortBy = "playList__title"
		elif objSortBy == u"Длине":
			#print("sortBy = length")
			sortBy = "length"
		if ubVozr == u"Возр":
			direction = ""
		if ubVozr == u"Убыв":
			direction = "-"
		form = FormSortBy(initial = {'objSort': objSortBy, 'ubVozr': ubVozr})
		form.fields['objSort'].choices = [
			('Названию','Названиию'), 
			('Исполнителю', 'Исполнителю'),
			('Плейлисту', 'Плейлисту'),
			('Длине', 'Длине')
		] 
		form.fields['ubVozr'].choices = [
			('Возр','Возр'), 
			('Убыв', 'Убыв')
		]
	#print("direction + sortBy = " + direction + sortBy)
	songs = FreeSong.objects.all().order_by(direction + sortBy)
	return render(request, 'showFreeAllSongs.html', { 'form': form, 'songs': songs })

@login_required
def add_free_song(request):
	playLists = FreePlayList.objects.all()
	choices = [('', '')]
	for playList in playLists:
		choices.append([playList.title, playList.title])
	form = FormSong()
	form.fields['playList'].choices = choices
	if request.POST:
		title = request.POST.get('title')
		singer = request.POST.get('singer')
		playList = request.POST.get('playList')
		songFile = request.FILES.get('songFile')
		albumImg = request.FILES.get('albumImg')
		print(title)
		print(singer)
		print(playList)
		#print("songFile = " + str(songFile))
		print(str(albumImg))
		print(albumImg)
		if isEmptyFields(title, singer, playList, songFile, albumImg):
			form = FormSong(initial = {'title': title, 'playList': playList, 'singer': singer})
			form.fields['playList'].choices = choices
			context = {
				'form': form,
				'is_empty_field': True,
			}
			return render(request, 'addFreeSong.html', context)
		else:
			### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			playListObj = FreePlayList.objects.get(title = playList)
			songObj = FreeSong(title = title, singer = singer, song_file = request.FILES.get('songFile'))
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
			saveFreeImg(songObj.id, title, albumImg.name, albumImg)
			audio = MP3(MEDIA_ROOT + "/" + str(songObj.song_file))
			#print("audio length = " + str(audio.info.length))
			songObj.length = int(round(audio.info.length))
			ssss = FreeSong.objects.filter(playList = playListObj).order_by("-pos")[:1]
			songObj.pos = ssss[0].pos + 1
			songObj.save()
			context = {
				'form': form,
				'add_successful': True
			}
			return redirect('/addfreesong/')
	return render(request, 'addFreeSong.html', { 'form': form })

@login_required
def show_free_songs(request, playlist_id):
	songs = FreeSong.objects.filter(playList__id = playlist_id).order_by('pos')
	return render(request, 'showFreeSongs.html', { 'songs': songs, 'playList': FreePlayList.objects.get(pk = playlist_id).title })

@login_required
def change_free_song(request, song_id):
	song = FreeSong.objects.get(pk = song_id)
	playLists = FreePlayList.objects.all()
	choices = [('', '')]
	for playList in playLists:
		choices.append([playList.title, playList.title])
	form = FormSong(initial={'title': song.title, 'pos': song.pos, 'singer': song.singer})
	form.fields['playList'].choices = choices 
	if request.POST:
		if request.POST.has_key('btn_save'):
			title = request.POST.get('title')
			singer = request.POST.get('singer')
			pos = request.POST.get('pos')
			playListTitle = request.POST.get('playList')
			songFile = request.FILES.get('songFile')
			albumImg = request.FILES.get('albumImg')
			#print(songFile)
			if isEmptyFields(title, singer, pos, playListTitle):
				context = {
					'form': form,
					'is_empty_field': True,
					'song': song,
				}
				return render(request, 'changeFreeSong.html', context)
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
					removeBlankSpaceInFreeList(song.pos, song.playList.id)
					song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
					song.playList.update_playlist.save()
					p = FreePlayList.objects.get(title = playListTitle)
					song.playList = p
					ssss = FreeSong.objects.filter(playList = p).order_by("-pos")[:1]
					#print(ssss)
					if len(ssss) != 0:
						song.pos = ssss[0].pos + 1
					else:
						song.pos = 1
				elif song.pos != int(pos):
					insertFreeSongToPos(song, int(pos))
				if song.title != title:
					renameFreeImg(song.id, song.title, title, song.expansion)
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
						deleteFreeImg(song.id, song.title, song.expansion)
						song.expansion = expansion_temp
					saveFreeImg(song.id, song.title, albumImg.name, albumImg)
				if not isEmptyFields(songFile):
					song.save()
					audio = MP3(MEDIA_ROOT + "/" + str(song.song_file))
					song.length = int(round(audio.info.length))
				if song.singer != singer:
					song.singer = singer
				#playList.title = title
				#playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				#playList.save()
				#playList.update_playlist.save()
				#form = FormPlayList(initial={'title': playList.title})
				song.save()
				song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
				song.playList.update_playlist.save()
				form = FormSong(initial={'title': song.title, 'pos': song.pos, 'singer': song.singer})
				form.fields['playList'].choices = choices
				context = {
					'form': form,
					'add_successful': True,
					'song': song
				}
				return render(request, 'changeFreeSong.html', context)
		elif request.POST.has_key('btn_delete'):
			#playList.delete()
			song.playList.update_playlist.last_update = int(datetime.now().strftime("%y%m%d%H%M%S"))
			song.playList.update_playlist.save()
			deleteFreeImg(song.id, song.title, song.expansion)
			path = os.path.join(MEDIA_ROOT, str(song.song_file))
			removeBlankSpaceInFreeList(song.pos, song.playList.id)
			#print("path: " + str(path))
			os.remove(path)
			song.delete()
			return redirect('/showfreesongs/' + str(song.playList.id) + '/')
		elif request.POST.has_key('btn_back'):
			print("btn_back")
			return redirect('/showfreesongs/' + str(song.playList.id) + '/')
	return render(request, 'changeFreeSong.html', { 'form': form, 'song': song })


#def clear_database(request):
	'''
	playLists = PlayList.objects.all()
	for playList in playLists:
		playList.delete()
	songs = Song.objects.all()
	for song in songs:
		song.delete()
	newUsers = NewUser.objects.all()
	for user in newUsers:
		user.delete()
	return HttpResponse("Clear")	
	'''
	#return HttpResponse('false')
	#return HttpResponse(MEDIA_ROOT)