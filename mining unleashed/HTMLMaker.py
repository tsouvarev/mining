#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plot
from hashlib import md5
from matplotlib import rc

class HTMLMaker:
	
	def __init__ (self, path_to_html, path_to_pics):
		
		self.path = path_to_html
		self.pics_path = path_to_pics
		self.pics_names = []
		self.html = "<html><body>"
		
#		rc('font',**{'family':'serif'})
#		rc('text', usetex=True)
#		rc('text.latex', unicode=True)
#		rc('text.latex', preamble='\usepackage[utf8]{inputenc}')
#		rc('text.latex', preamble='\usepackage[russian]{babel}')


	def add_figure (self, data, title):

		plot.clf ()
	
		filename = self.pics_path + md5(title).hexdigest() + ".png"
	
		if title is not None: plot.title (unicode (title))
	
		plot.plot (data)
		plot.savefig (filename, format = "png")
		
		self.pics_names.append (filename)
		self.html += "<img src='%s'>" % filename
	
	def add_break (self):
	
		self.html += "<br />"
		
	def add_line (self):
	
		self.html += "<hr /><br />"
	
	def save (self):

		self.html += "</body></html>"

		fd = open (self.path + "index.html", "w")
		fd.write (self.html)
		fd.close ()
		
		self.html = "<html><body>"
