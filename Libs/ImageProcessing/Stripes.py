#! /usr/bin/python
# -*- coding: utf-8 -*-

from Libs.Analytics.Core import re, amp, comp, im, maximum, convolve as conv, f as fourier, correlation, derivative
from Libs.Analytics.Filters import *
from numpy import zeros, empty, append
from PIL import Image

def remove_stripes (i):

	w,h = i.size
	i = i.load()

	out = empty (0)
	freqs = []
	
	dl = 5
	step = 15

	for y in range (0, h-dl, step):

		a = derivative ([i[x, y] for x in range (w)])
		b = derivative ([i[x, y+dl] for x in range (w)])
		
		corr = correlation (a,b)
		
		f = fourier (corr)

		freq, ind = max(maximum (f[:,amp], l = len(f)//20, r = len(f)//2))
		
		ind = ind / float (len(f)//2) *0.5	
		
#		print freq
		
		freqs.append (ind)

	freq_avg = sum (freqs)/len (freqs)
	dfreq = 0.01
	
	print freq_avg, dfreq
	
	filt = lpf (freq_avg-dfreq, dt=1, m=64)

	for y in range (h):

		a = [i[x, y] for x in range (w)]
		
		out = append (out, conv (a, filt))

	# сохраняем новое изображение
	img = Image.new ("L", (w,h))
	img.putdata (out)

	return img
