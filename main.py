#! /usr/bin/python
# -*- coding: utf-8 -*-

from libs.HTMLMaker import HTMLMaker
from libs.maintenance import autocorrelation as auto, fourier, re,amp,comp,im, maximum, conv
from libs.filters import *
from libs.kespr_reader import convert as kespr2bmp
from time import time
from os.path import abspath as path, basename as base
from labs.hist_eq import hist_eq
from numpy import zeros, empty, append
from math import sin, pi
from PIL import Image

html = HTMLMaker ("./", "pics_out/")

t0 = time()

pic = "/home/minime/Desktop/mining/pics_in/XRx1024_clear.jpg"
html.add_picture (pic, width = 500)

i = Image.open (pic)
w,h = i.size
i = i.load()

out = empty (0)

######### вкратце содержание серии: считаем частоту, на которой находятся полоски, и которую потом будем вырезать
a = [i[y, 0] for y in range (w)]
f = fourier (a)

# в преобразовании фурье находим пики (значит, на этой частоте соотв. периодичность)
# из всех пиков выбираем максимальный и запоминаем его индекс
# пропускаем первые 30 значений (не меньше 10, там трэшак творится)
# и идем до середины массива (у фурье половины зеркально симметричны)
freq, ind = max(maximum (f[:,amp], l = 30, r = len(f)//2))
# масштабируем индекс по шкале [0;0.5]
ind = ind / float (len(f)//2) *0.5
# фильтровать будем режекторным фильтром, задаем ему небольшую рамку вокруг нашей частоты
filt = bsf (ind-0.2, ind+0.1, dt=1)

# применяем свертку к изображению построчно
# вопрос: нужна ли тут двумерная свертка, если и так все работает?
for y in range (h):

	a = [i[x, y] for x in range (w)]
	out = append (out, conv (a, filt))

# сохраняем новое изображение
img = Image.new("L", (w,h))
img.putdata (out)
img.save ("pics_out/out.jpg", "JPEG")
html.add_picture ("pics_out/out.jpg", width = 500)

print time() - t0

html.save ()



























