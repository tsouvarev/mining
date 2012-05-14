#! /usr/bin/python
# -*- coding: utf-8 -*-

from Libs.HTMLMaker import HTMLMaker
from Libs.ImageProcessing.Stripes import remove_stripes
from Libs.ImageProcessing.HistogrammEqualization import hist_eq as equalize
from Libs.ImageProcessing.Stripes import remove_stripes
from Libs.Analytics.Core import f as fourier, convolve, amp
from Libs.Analytics.Filters import *
from time import time
from os.path import abspath as path, basename as base
from os import remove
from PIL import Image
from math import sin, cos, pi

html = HTMLMaker ("./", "PicsOut/")

t0 = time()

pic = "/home/minime/Desktop/mining/Pics/XR_clear.jpg"
#pic = "/home/minime/Desktop/mining/Pics/XR_clear.jpg"
#html.add_picture (pic, width = 500)

i = Image.open (pic)

#img = remove_stripes (i)

#try: remove ("./PicsOut/out.jpg")
#except: pass

#img.save ("/home/minime/Desktop/mining/PicsOut/out.bmp", "BMP")
#html.add_picture ("PicsOut/out.bmp", width = 500)

out = open ("./PicsOut/out_new.bmp", "w+")
stripes = open ("./PicsOut/stripes_out.bmp", "w+")
differ = open ("./PicsOut/diff.bmp", "w+")

######################## code for detecting pikes on autocorrelation of derivatives

w,h = i.size
#i = i.load()

r = equalize (i)

r["new"].save (out)
html.add_picture ("./PicsOut/out_new.bmp", title = "Image")

out = remove_stripes (r["new"])
out.save (stripes)
html.add_picture ("./PicsOut/stripes_out.bmp", title = "Stripped image")

r = r["new"].load()
out = out.load()

diff = Image.new ("L", (w,h))
diff.putdata ([(out[x,y] - r[x,y])*30 for y in range (h) for x in range (w)])

diff.save (differ)
html.add_picture ("./PicsOut/diff.bmp", title = "Difference")

#out.close()
#stripes.close()

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


print time() - t0

html.save ()






























