from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PlayList(models.Model):
	title = models.CharField(max_length = 30)

	def __unicode__(self):
		return (str(self.id) + ' ' + self.text)


class Song(models.Model):
	# !!!!!!!!!!!!!!!!!!1111
	playList = models.ForeignKey(
		PlayList, 
		on_delete = models.SET_NULL, 
		blank = True,
		null = True
	)
	title = models.CharField(max_length = 20)
	#auto_now = True
	length = models.TimeField(null = True)
	song_file = models.FileField(upload_to = 'songs/', null = True)
	album_img = models.ImageField(upload_to = "album_img/", null = True)

	def __unicode__(self):
		return (str(self.id) + ' ' + self.title)
