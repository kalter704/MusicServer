from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth.models import User

# Create your models here.

class PlayList(models.Model):
	title = models.CharField(max_length = 50)
	pos = models.IntegerField(default = 0)
	schoolOwner = models.CharField(max_length = 50)

	def __unicode__(self):
		return (str(self.id) + ' ' + self.title)

	def __str__(self):
		return ('id: ' + str(self.id) + '; ' + self.title + '; update_playlist = ' + str(self.update_playlist.last_update))


class Song(models.Model):
	# !!!!!!!!!!!!!!!!!!1111
	playList = models.ForeignKey(
		PlayList, 
		on_delete = models.SET_NULL, 
		blank = True,
		null = True,
		related_name = 'songs'
	)
	title = models.CharField(max_length = 50)
	#auto_now = True
	#length = models.TimeField(null = True)
	length = models.IntegerField(default = -1)
	song_file = models.FileField(upload_to = 'songs/', null = True)
	#album_img_title = models.CharField(max_length = 30)
	#album_img = models.ImageField(upload_to = "album_img/", null = True)
	pos = models.IntegerField(default = 0)
	expansion = models.CharField(max_length = 5)
	singer = models.CharField(max_length = 50, default = "")

	def __unicode__(self):
		return (str(self.id) + ' ' + self.title)

	def __str__(self):
		#return (self.title)
		if (self.playList != None):
			return (self.title + ' PlayList: ' + str(self.playList.title))
		else:
			return (self.title + ' PlayList: null')


class UdpatePlayList(models.Model):
	last_update = models.BigIntegerField()
	playList = models.OneToOneField(PlayList, on_delete = models.CASCADE, related_name = 'update_playlist')

	def __unicode__(self):
		return (str(self.id) + '; ' + 'PlayList: ' + str(self.playList.title) + '; Last update: ' + str(self.last_update))

	def __str__(self):
		return (str(self.id) + '; ' + 'PlayList: ' + str(self.playList.title) + '; Last update: ' + str(self.last_update))

class NewUser(models.Model):
	name = models.CharField(max_length = 50)
	password = models.CharField(max_length = 20)

	def __unicode__(self):
		return (str(self.id) + '; ' + 'Name: ' + self.name)

	def __str__(self):
		return (str(self.id) + '; ' + 'Name: ' + self.name)


class Ads(models.Model):
	name = models.CharField(max_length = 30)
	img = models.ImageField(upload_to = 'ads/', null = True)
	# 1 - show, 2 - not show
	state = models.IntegerField(default = -1)
	# 1 - interstitial, 2 - banner
	ad_type = models.IntegerField(default = -1)
	url = models.CharField(max_length = 80, default = "")


class UserType(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'user_type')
	type = models.IntegerField(default = 0)


class MobAppVersion(models.Model):
	android_app = models.IntegerField(default = -1)
	ios_app = models.IntegerField(default = -1)


class FreePlayList(models.Model):
	title = models.CharField(max_length = 50)
	pos = models.IntegerField(default = 0)
	schoolOwner = models.CharField(max_length = 50)

	def __unicode__(self):
		return (str(self.id) + ' ' + self.title)

	def __str__(self):
		return ('id: ' + str(self.id) + '; ' + self.title + '; update_playlist = ' + str(self.update_playlist.last_update))


class FreeSong(models.Model):
	# !!!!!!!!!!!!!!!!!!1111
	playList = models.ForeignKey(
		FreePlayList, 
		on_delete = models.SET_NULL, 
		blank = True,
		null = True,
		related_name = 'songs'
	)
	title = models.CharField(max_length = 50)
	#auto_now = True
	#length = models.TimeField(null = True)
	length = models.IntegerField(default = -1)
	song_file = models.FileField(upload_to = 'songs/free_songs/', null = True)
	#album_img_title = models.CharField(max_length = 30)
	#album_img = models.ImageField(upload_to = "album_img/", null = True)
	pos = models.IntegerField(default = 0)
	expansion = models.CharField(max_length = 5)
	singer = models.CharField(max_length = 50, default = "")

	def __unicode__(self):
		return (str(self.id) + ' ' + self.title)

	def __str__(self):
		#return (self.title)
		if (self.playList != None):
			return (self.title + ' FreePlayList: ' + str(self.playList.title))
		else:
			return (self.title + ' FreePlayList: null')


class UdpateFreePlayList(models.Model):
	last_update = models.BigIntegerField()
	playList = models.OneToOneField(FreePlayList, on_delete = models.CASCADE, related_name = 'update_playlist')

	def __unicode__(self):
		return (str(self.id) + '; ' + 'FreePlayList: ' + str(self.playList.title) + '; Last update: ' + str(self.last_update))

	def __str__(self):
		return (str(self.id) + '; ' + 'FreePlayList: ' + str(self.playList.title) + '; Last update: ' + str(self.last_update))
