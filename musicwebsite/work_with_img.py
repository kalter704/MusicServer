# -*- coding: utf-8 -*-
import os
from MusicServer.settings import MEDIA_ROOT

def save_img(title, img):
	with open(os.path.join(MEDIA_ROOT, title + "mdpi.png"), 'wb+') as dest:
		for chunk in img.chunks():
			dest.write(chunk)
	return True