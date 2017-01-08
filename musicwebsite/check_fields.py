# -*- coding: utf-8 -*-

def isEmptyFields(*args):
	for a in args:
		if a == '':
			return True
	return False