#! /usr/bin/python
# -*- coding: utf-8 -*-

from libs.HTMLMaker import HTMLMaker
from libs.maintenance import autocorrelation as auto, fourier, re,amp,comp,im, maximum
from time import time
from os.path import abspath as path, basename as base
from labs.hist_eq import hist_eq
from numpy import zeros
from math import sin, pi
from PIL import Image

html = HTMLMaker ("./", "pics_out/")

t0 = time()

#hist_eq (path ("pics_in/XRx1024.jpg"), html)
#hist_eq ("XR.jpg")
#hist_eq (path ("pics_in/b.jpg"), html)
i = Image.open (path ("pics_in/XRx1024.jpg"))
w,h = i.size
i = i.load()

#a = [sin (2 * pi * 100 * x * 0.001)+sin (2 * pi * 200 * x * 0.001) for x in range (100)]

for x in range (1):

	a = [i[y, x] for y in range (w)]

	f = fourier (a)

	html.add_figure (auto (a), u"Auto")
	html.add_figure (f[:,amp], u"Fourier")#, dt=0.001)
	print max(maximum (f[:,amp], l = 30, r = len(f)//2))
#	print len (f[10:-10,amp])

print time() - t0

html.save ()



























