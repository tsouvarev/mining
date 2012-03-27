#! /usr/bin/python
# -*- coding: utf-8 -*-

from Libs.HTMLMaker import HTMLMaker
from Libs.ImageProcessing.Stripes import remove_stripes
from time import time
from os.path import abspath as path, basename as base
from os import remove
from PIL import Image

html = HTMLMaker ("./", "PicsOut/")

t0 = time()

pic = "/home/minime/Desktop/mining/Pics/XRx1024_clear.jpg"
#pic = "/home/minime/Desktop/mining/Pics/XR_clear.jpg"
html.add_picture (pic, width = 500)

i = Image.open (pic)

img = remove_stripes (i)

#try: remove ("./PicsOut/out.jpg")
#except: pass

img.save ("/home/minime/Desktop/mining/PicsOut/out.bmp", "BMP")
html.add_picture ("PicsOut/out.bmp", width = 500)

print time() - t0

html.save ()



























