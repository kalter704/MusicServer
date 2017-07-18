# -*- coding: utf-8 -*-
from django import forms

class FormPlayList(forms.Form):
	title = forms.CharField(label='Название плейлиста:', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	schoolOwner = forms.CharField(label='Название школы:', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	pos = forms.IntegerField(label = 'Позиция:', widget = forms.NumberInput(attrs = {'class': 'form-control'}))

class FormSong(forms.Form):
	playList = forms.ChoiceField(label = 'Плейлист:', widget = forms.Select(attrs = {'class': 'form-control'}))
	title = forms.CharField(label = 'Название песни:', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	singer = forms.CharField(label = 'Исполнитель:', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	songFile = forms.FileField(label = 'Песня:', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'checkSongURL(this)'}))
	albumImg = forms.ImageField(label = 'Картинка:', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'checkImgURL(this)'}))
	pos = forms.IntegerField(label = 'Позиция:', widget = forms.NumberInput(attrs = {'class': 'form-control'}))

class FormRegisterUser(forms.Form):
	login = forms.CharField(label='Логин:', widget = forms.TextInput(attrs = {'class': 'form-control filds_width_center'}))
	password = forms.CharField(label='Пароль:', widget = forms.PasswordInput(attrs = {'class': 'form-control filds_width_center'}))
	password2 = forms.CharField(label='Повторите пароль:', widget = forms.PasswordInput(attrs = {'class': 'form-control filds_width_center'}))

class FormLogInUser(forms.Form):
	login = forms.CharField(label='Логин:', widget = forms.TextInput(attrs = {'class': 'form-control filds_width_center'}))
	password = forms.CharField(label='Пароль:', widget = forms.PasswordInput(attrs = {'class': 'form-control filds_width_center'}))

class FormSortBy(forms.Form):
	 objSort= forms.ChoiceField(label = 'Сортировака по:', widget = forms.Select(attrs = {'class': 'form-control'}))
	 ubVozr = forms.ChoiceField(label = 'Убыв/Возр:', widget = forms.Select(attrs = {'class': 'form-control'}))

class FormAd(forms.Form):
	title = forms.CharField(label = 'Название рекламы:', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	img = forms.ImageField(label = 'Картинка:', widget = forms.ClearableFileInput(attrs = {'class': 'form-control'}))
	ad_type = forms.CharField(label = 'Тип рекламы:', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	url = forms.CharField(label = 'Ссылка:', widget = forms.TextInput(attrs = {'class': 'form-control'}))

class FormMobAppVersion(forms.Form):
	androidVersion = forms.IntegerField(label = 'Версия андроид приложения:', widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	iosVersion = forms.IntegerField(label = 'Версия ios приложения:', widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	