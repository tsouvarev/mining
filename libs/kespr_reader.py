#! /usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import array, empty, zeros
from struct import unpack
from time import time

def convert (filename_in, filename_out):

	f = open (filename_in, "rb")
	
	w, h = 2048, 2500
	size = (w, h)
	
	out = Image.new ("L", size)
	out_p = out.load ()
	
	f.seek (2048)
	
	arr = empty (w*h)
	
	for i in range (w*h): 
	
		c1, c2, = unpack ('>BB', f.read (2))
	
#		print unpack ('>H', c)
		
#		arr[i], = unpack ('>H', c)
		arr[i] = c1 + c2 << 8
	
	arr /= 65536. 
	arr *= 255
	
	out.putdata (arr)
	out = out.transpose (Image.ROTATE_90)
	out.save (filename_out, "BMP")

