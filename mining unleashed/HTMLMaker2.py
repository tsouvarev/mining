#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plot
from hashlib import md5
from matplotlib import rc

pics_names = []
html = "<html><body>"

def add_figure (data, title):

	global pics_names, html
	
	plot.clf ()

	filename = "pics/" + md5(title).hexdigest() + ".png"

	if title is not None: plot.title (unicode (title))

	plot.plot (data)
	plot.savefig (filename, format = "png")
	
	pics_names.append (filename)
	html += "<img src='%s'>\n" % filename

def add_break ():

	global html
	html += "<br />\n"
	
def add_line ():

	global html
	html += "<hr /><br />\n"

def save (path_to_html, path_to_pics):

	global html
	html += "</body></html>"

	fd = open (path_to_html + "index.html", "w")
	fd.write (html)
	fd.close ()
	
	html = "<html><body>"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
