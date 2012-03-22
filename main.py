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

i = Image.open (path ("/home/minime/Desktop/mining/pics_in/XRx1024_clear.jpg")) # 
#out = Image.new (i.size)
#out_p = out.load()



w,h = i.size
i = i.load()

out = empty (0)

#a = [sin (2 * pi * 100 * x * 0.001)+sin (2 * pi * 200 * x * 0.001) for x in range (100)]
a = [i[y, 0] for y in range (w)]
f = fourier (a)

freq, ind = max(maximum (f[:,amp], l = 30, r = len(f)//2))

print ind

ind = ind / float (len(f)//2) *0.5

print ind

filt = bsf (ind-0.2, ind+0.1, dt=1)

for y in range (h):

	a = [i[x, y] for x in range (w)]
	out = append (out, conv (a, filt))

img = Image.new("L", (w,h))
img.putdata (out)
img.save ("pics_out/out.jpg", "JPEG")

#kespr2bmp (	"/home/minime/Desktop/mining/pics_in/Xray.kcr", 
#		"/home/minime/Desktop/mining/pics_out/Xray.bmp")

print time() - t0

html.save ()



























