#! /usr/bin/python
# -*- coding: utf-8 -*-

from libs.HTMLMaker import HTMLMaker
from time import time
from os.path import abspath as path, basename as base
from labs.hist_eq import hist_eq

html = HTMLMaker ("./", "pics_out/")

t0 = time()

#hist_eq ("XRx1024.jpg")
#hist_eq ("XR.jpg")
hist_eq (path ("pics_in/b.jpg"), html)

print time() - t0

html.save ()



























