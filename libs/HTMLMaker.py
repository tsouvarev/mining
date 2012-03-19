#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plot
from hashlib import md5
from matplotlib import rc
from matplotlib.figure import Figure as fig
from random import random

class HTMLMaker:
	
	def __init__ (self, path_to_html, path_to_pics):
		
		self.i = 1
		
		self.path = path_to_html
		self.pics_path = path_to_pics
		self.pics_names = []
		self.html = "<html><body>"
		
	def add_figure (self, data, title, dt = None, width = None, height = None):

		plot.clf ()

#		filename = self.pics_path + str(self.i) + ".png"
		filename = self.pics_path + md5(title.encode('utf-8') + str (random())).hexdigest() + ".png"
#		filename = self.pics_path + title.encode('utf-8') + ".png"
	
		if title is not None: plot.title (unicode (title))
	
		if dt is not None: 
			
			N = len (data)
			axis = [float(i)/(dt*N) for i in range(N)]
			plot.plot (axis, data)
		
		else: plot.plot (data)	
		
		plot.grid (True)
		plot.savefig (filename, format = "png")
		
		self.pics_names.append (filename)
		self.html += "<img src='%s'" % filename
		
		if width is not None: self.html += " width='%s'" % width
		elif height is not None: self.html += " height='%s'" % height
		
		self.html += ">"
		
	def add_table (self, tdata, title):
	
		self.html += "<table style='font-size: xx-large; \
									margin: 15px; \
									float: left; \
									border: 1px solid;\
									border-spacing: 15px;\
									cellspacing: 15px;'>"
		self.html += "<caption>%s</caption>" % title.encode ("utf-8")
		
		for row in tdata:
		
			self.html += "<tr>"
			
			for cell in row: self.html += str (cell)
			#self.html += "<td style='margin: 25px;'>%s</td>" % cell
			
			self.html += "</tr>"
		
		self.html += "</table>"
		
	def add_clear (self):
	
		self.html += "<div style='clear: both;'></div>"
	
	def add_picture (self, filename, width = None, height = None):
	
		self.pics_names.append (filename)
		
		self.html += "<img src='%s'" % filename
		
		if width is not None: self.html += " width='%s'" % width
		elif height is not None: self.html += " height='%s'" % height
		
		self.html += ">"
	
	def add_break (self):
	
		self.html += "<br />"
		
	def add_line (self):
	
		self.html += "<hr /><br />"
		
	def add_text (self, t):
	
		self.html += "<br /><h1>" + t.encode('utf-8') + "</h1><br />"
	
	def save (self):

		self.html += "</body></html>"

		fd = open (self.path + "index.html", "w")
		fd.write (self.html)
		fd.close ()
		
		self.html = "<html><body>"
