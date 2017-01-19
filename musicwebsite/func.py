# -*- coding: utf-8 -*-
import os
from MusicServer.settings import MEDIA_ROOT
from PIL import Image
from constants import *
from models import PlayList, Song, NewUser
from django.contrib.auth.models import User


def isEmptyFields(*args):
	for a in args:
		if a == '' or a == None:
			return True
	return False

def isExistUser(name):
	try:
		u = User.objects.get(username = name)
	except:
		u = None
	try:
		nu = NewUser.objects.get(name = name)
	except:
		nu = None
	if (u == None) and (nu == None):
		return False
	else:
		return True

def insertPlaylistToPos(playList, pos):
	i = playList.pos
	#playListId = playList.id
	#print('i = ' + str(i))
	#print('pos = ' + str(pos))
	if i > pos:
		isUp = True
		i -= 1
	else:
		isUp = False
		i += 1
	#print('isUp = ' + str(isUp))
	try:
		p = PlayList.objects.get(pos = i)
	except:
		p = None
	while (i != pos) and (p != None):
		if isUp:
			p.pos = i + 1
			i -= 1
		else:
			p.pos = i - 1
			i += 1
		p.save()
		try:
			p = PlayList.objects.get(pos = i)
		except:
			p = None
	#print(p)
	if p == None:
		if isUp:
			i += 1
		else:
			i -= 1
		pos = i
	elif pos == i:
		if isUp:
			p.pos = i + 1
		else:
			p.pos = i - 1
		p.save()
	playList.pos = pos
	#playList.save()

def insertSongToPos(song, pos):
	i = song.pos
	playList_id = song.playList.id
	#print("i = " + str(i))
	#print("pos = " + str(pos))
	if i > pos:
		isUp = True
		#print("bef i = " + str(i))
		i -= 1
		#print("aft i = " + str(i))
	else:
		isUp = False
		i += 1
	#print("i = " + str(i))
	try:
		s = Song.objects.filter(playList__id = playList_id).get(pos = i)
	except:
		s = None
	#print("s == " + str(s))
	while (i != pos) and (s != None):
		#print("i = " + str(i))
		if isUp:
			s.pos = i + 1
			i -= 1
		else:
			s.pos = i - 1
			i += 1
		s.save()
		try:
			s = Song.objects.filter(playList__id = playList_id).get(pos = i)
		except:
			s = None
	#print("i = " + str(i))
	#print("s == " + str(s))
	#print("pos = " + str(pos))
	if s == None:
		if isUp:
			i += 1
		else:
			i -= 1
		pos = i
	elif i == pos:
		if isUp:
			s.pos = i + 1
		else:
			s.pos = i - 1
		s.save()
	#print("song.pos = pos = " + str(pos))	
	song.pos = pos
	#song.save()

def removeBlankSpaceInList(pos, playList_id):
	pos += 1
	try:
		s = Song.objects.filter(playList__id = playList_id).get(pos = pos)
	except:
		s = None
	while s != None:
		s.pos = pos - 1
		s.save()
		pos += 1
		try:
			s = Song.objects.filter(playList__id = playList_id).get(pos = pos)
		except:
			s = None

def saveImg(id, title, img_name, img):
	path = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + title)
	if img_name.endswith(".jpg"):
		expansion = ".jpg"
	elif img_name.endswith(".jpeg"):
		expansion = ".jpeg"
	elif img_name.endswith(".png"):
		expansion = ".png"

	with open(path + "xxxhdpi" + expansion, 'wb+') as dest:
		for chunk in img.chunks():
			dest.write(chunk)

	old_img = Image.open(path + "xxxhdpi" + expansion)
	new_img = old_img.resize((XXXHDPI_WIDTH, XXXHDPI_WIDTH), Image.ANTIALIAS)
	new_img.save(path + "xxxhdpi" + expansion)


	with open(path + "xxhdpi" + expansion, 'wb+') as dest:
		for chunk in img.chunks():
			dest.write(chunk)

	old_img = Image.open(path + "xxhdpi" + expansion)
	new_img = old_img.resize((XXHDPI_WIDTH, XXHDPI_WIDTH), Image.ANTIALIAS)
	new_img.save(path + "xxhdpi" + expansion)


	with open(path + "xhdpi" + expansion, 'wb+') as dest:
		for chunk in img.chunks():
			dest.write(chunk)

	old_img = Image.open(path + "xhdpi" + expansion)
	new_img = old_img.resize((XHDPI_WIDTH, XHDPI_WIDTH), Image.ANTIALIAS)
	new_img.save(path + "xhdpi" + expansion)


	with open(path + "hdpi" + expansion, 'wb+') as dest:
		for chunk in img.chunks():
			dest.write(chunk)

	old_img = Image.open(path + "hdpi" + expansion)
	new_img = old_img.resize((HDPI_WIDTH, HDPI_WIDTH), Image.ANTIALIAS)
	new_img.save(path + "hdpi" + expansion)


	with open(path + "mdpi" + expansion, 'wb+') as dest:
		for chunk in img.chunks():
			dest.write(chunk)

	old_img = Image.open(path + "mdpi" + expansion)
	new_img = old_img.resize((MDPI_WIDTH, MDPI_WIDTH), Image.ANTIALIAS)
	new_img.save(path + "mdpi" + expansion)

	return True

def renameImg(id, oldTitle, newTitle, expansion):
	oldPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + oldTitle + 'xxxhdpi.' + expansion)
	newPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + newTitle + 'xxxhdpi.' + expansion)
	os.rename(oldPath, newPath)

	oldPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + oldTitle + 'xxhdpi.' + expansion)
	newPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + newTitle + 'xxhdpi.' + expansion)
	os.rename(oldPath, newPath)

	oldPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + oldTitle + 'xhdpi.' + expansion)
	newPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + newTitle + 'xhdpi.' + expansion)
	os.rename(oldPath, newPath)

	oldPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + oldTitle + 'hdpi.' + expansion)
	newPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + newTitle + 'hdpi.' + expansion)
	os.rename(oldPath, newPath)

	oldPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + oldTitle + 'mdpi.' + expansion)
	newPath = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + newTitle + 'mdpi.' + expansion)
	os.rename(oldPath, newPath)


def deleteImg(id, title, expansion):
	path = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + title + 'xxxhdpi.' + expansion)
	os.remove(path)

	path = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + title + 'xxhdpi.' + expansion)
	os.remove(path)

	path = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + title + 'xhdpi.' + expansion)
	os.remove(path)

	path = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + title + 'hdpi.' + expansion)
	os.remove(path)

	path = os.path.join(MEDIA_ROOT, "album_img/" + str(id) + '_' + title + 'mdpi.' + expansion)
	os.remove(path)
