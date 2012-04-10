#! /usr/bin/python
# -*- coding: utf-8 -*-

from Libs.HTMLMaker import HTMLMaker
from Libs.ImageProcessing.Stripes import remove_stripes
from Libs.Analytics.Core import *
from Libs.Analytics.Filters import *
from time import time
from os.path import abspath as path, basename as base
from os import remove
from PIL import Image

html = HTMLMaker ("./", "PicsOut/")

t0 = time()

pic = "/home/minime/Desktop/mining/Pics/XRx1024_clear.jpg"
#pic = "/home/minime/Desktop/mining/Pics/XR_clear.jpg"
#html.add_picture (pic, width = 500)

i = Image.open (pic)

#img = remove_stripes (i)

#try: remove ("./PicsOut/out.jpg")
#except: pass

#img.save ("/home/minime/Desktop/mining/PicsOut/out.bmp", "BMP")
#html.add_picture ("PicsOut/out.bmp", width = 500)

######################## code for detecting pikes on autocorrelation of derivatives

w,h = i.size
i = i.load()

#a = array ([i[x,0] for x in range (w)])
#d = derivative (a)
#ac = autocorrelation (d)
#f = fourier (ac)
#
#html.add_figure (ac,u"autocorr")
#html.add_figure (f, u"fourier")
#
#print max(maximum (f[:,amp], l = len(f)//20, r = len(f)//2))
#
###################################

f = fourier (bsf (0.3, 0.1, m = 256, dt = 1))

html.add_figure (data = f[:len(f)//2, amp], title = "bsf")

print time() - t0

html.save ()





























