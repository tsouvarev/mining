#! /usr/bin/python
# -*- coding: utf-8 -*-

from Libs.Analytics.Core import re, amp, comp, im, maximum, convolve as conv, f as fourier
from Libs.Analytics.Filters import *
from numpy import zeros, empty, append
from PIL import Image

def remove_stripes (i):

	w,h = i.size
	i = i.load()

	out = empty (0)

	## вкратце содержание серии: считаем частоту, на которой находятся полоски, и которую потом будем вырезать
#	a = [i[y, 0] for y in range (w)]
#	f = fourier (a)

	# в преобразовании фурье находим пики (значит, на этой частоте соотв. периодичность)
	# из всех пиков выбираем максимальный и запоминаем его индекс
	# пропускаем двадцатую (полурандомное число, взято из тестовых заходов) часть интервала 
	# (но не меньше 10, там трэшак творится)
	# и идем до середины массива (у фурье половины зеркально симметричны)
#	freq, ind = max(maximum (f[:,amp], l = len(f)//20, r = len(f)//2))

	# масштабируем индекс по шкале [0;0.5]
	# вопрос: брать весь интервал, по которому раскидано преобразование Фурье или только половину
	# (по идее, значащая только половина, вторая половина есть зеркальное отображение первой)
	# сейчас берется только половина
#	ind = ind / float (len(f)//2) *0.5

#	print ind, freq

	# фильтровать будем режекторным фильтром, задаем ему небольшую рамку вокруг нашей частоты
#	filt = bsf (ind-0.03, ind+0.03, dt=1, m=32)

	# применяем свертку к изображению построчно
	# вопрос: нужна ли тут двумерная свертка, если и так все работает?
	for y in range (h):

		a = [i[x, y] for x in range (w)]
		f = fourier (a)

		freq, ind = max(maximum (f[:,amp], l = len(f)//20, r = len(f)//2))
		
		ind = ind / float (len(f)//2) *0.5	
		
		if y // 15 == 0: print freq

		filt = bsf (ind-0.2, ind+0.1, dt=1, m=32, truncate = True)
		out = append (out, conv (a, filt))

	# сохраняем новое изображение
	img = Image.new ("L", (w,h))
	img.putdata (out)

	return img
