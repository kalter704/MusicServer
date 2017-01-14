# -*- coding: utf-8 -*-
from models import PlayList, Song


def isEmptyFields(*args):
	for a in args:
		if a == '' or a == None:
			return True
	return False

def insertSongToPos(song, pos):
	i = song.pos
	playList_id = song.playList.id
	print("i = " + str(i))
	print("pos = " + str(pos))
	if i > pos:
		isUp = True
		print("bef i = " + str(i))
		i -= 1
		print("aft i = " + str(i))
	else:
		isUp = False
		i += 1
	print("i = " + str(i))
	try:
		s = Song.objects.filter(playList__id = playList_id).get(pos = i)
	except:
		s = None
	print("s == " + str(s))
	while (i != pos) and (s != None):
		print("i = " + str(i))
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
	print("i = " + str(i))
	print("s == " + str(s))
	print("pos = " + str(pos))
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
	print("song.pos = pos = " + str(pos))	
	song.pos = pos
	song.save()

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