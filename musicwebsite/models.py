from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User

# Create your models here.

class PlayList(models.Model):
	title = models.CharField(max_length = 30)
	pos = models.IntegerField(default = 0)
	schoolOwner = models.CharField(max_length = 30)

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
	title = models.CharField(max_length = 20)
	#auto_now = True
	#length = models.TimeField(null = True)
	length = models.IntegerField(default = -1)
	song_file = models.FileField(upload_to = 'songs/', null = True)
	#album_img_title = models.CharField(max_length = 30)
	#album_img = models.ImageField(upload_to = "album_img/", null = True)
	pos = models.IntegerField(default = 0)
	expansion = models.CharField(max_length = 5)

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
	name = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)

	def __unicode__(self):
		return (str(self.id) + '; ' + 'Name: ' + self.name)

	def __str__(self):
		return (str(self.id) + '; ' + 'Name: ' + self.name)