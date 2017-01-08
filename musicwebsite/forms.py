# -*- coding: utf-8 -*-
from django import forms

class FormPlayList(forms.Form):
	title = forms.CharField(label='Название плейлиста', widget = forms.TextInput(attrs = {'class': 'form-control'}))

class FormSong(forms.Form):
	playList = forms.ChoiceField(label = 'Плейлист', widget = forms.Select(attrs = {'class': 'form-control'}))
	title = forms.CharField(label = 'Название песни', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	#length = forms.CharField(label = 'Длина', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	songFile = forms.FileField(label = 'Песня', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'checkSongURL(this)'}))
	albumImg = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'checkImgURL(this)'}))
	'''
	albumImgMDPI = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control invisible_field'}))
	albumImgHDPI = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control invisible_field'}))
	albumImgXHDPI = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control invisible_field'}))
	albumImgXXHDPI = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control invisible_field'}))
	albumImgXXXHDPI = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control invisible_field'}))
	'''
	
		