# -*- coding: utf-8 -*-
import os
from MusicServer.settings import MEDIA_ROOT
from PIL import Image
from constants import *

def save_img(id, title, img_name, img):
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