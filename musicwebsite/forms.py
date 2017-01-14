# -*- coding: utf-8 -*-
from django import forms

class FormPlayList(forms.Form):
	title = forms.CharField(label='Название плейлиста', widget = forms.TextInput(attrs = {'class': 'form-control'}))

class FormSong(forms.Form):
	playList = forms.ChoiceField(label = 'Плейлист', widget = forms.Select(attrs = {'class': 'form-control'}))
	title = forms.CharField(label = 'Название песни', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	songFile = forms.FileField(label = 'Песня', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'checkSongURL(this)'}))
	albumImg = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'checkImgURL(this)'}))
	pos = forms.IntegerField(label = 'Позиция', widget = forms.NumberInput(attrs = {'class': 'form-control'}))