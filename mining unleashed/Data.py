#! /usr/bin/python
# -*- coding: utf-8 -*-

import HTMLMaker2 as html
from math import sin, cos, pi, sqrt, exp

class test ():

	def __init__ (self):
	
		self.a = 0
		self.n = []
	
	def __str__ (self):
	
		return str (self.a)
		
	def push (self, n):
	
		self.n.append (n)
	
	def add (self, n):
		
		self.a += n
		return self


class Data ():

	def __init__ (self, data, name):
	
		self.name = name
		self.data = data
		self.N = len (data)
		self.current = data
		self.current_name = ""
		
		self.f = {	"re": [],
					"im": [],
					"comp": [],
					"amp": []
					}
		
		self.conv_f = {	"re": [],
						"im": [],
						"comp": [],
						"amp": []
						}
		self.comp = None
		
		self.inv = []
		self.conv_t = []
		
	def fourier (self):
	
		if len (self.f["re"]) > 0: return self
		
		for j in range (self.N):
	
			r = 0.0; i = 0.0; a = 0.0; c = 0.0
	
			for k in range (self.N):
			
				r += self.data[k] * cos (2.0 * pi * k * j / self.N)
				i += self.data[k] * sin (2.0 * pi * k * j / self.N)
		
			a = sqrt (r*r + i*i)
			c = r - i
		
			self.f["re"].append (r)
			self.f["im"].append (i)
			self.f["amp"].append (a)
			self.f["comp"].append (c)		
		
		self.comp = self.f["comp"]
		self.current = self.f["comp"]
		self.current_name = "fourier_complex_spectre"
		
		return self
	
	def fourier_inv (self):

		if len (self.inv) > 0: return self
		self.N = len (self.comp)
		
		#print len (self.comp)#.N
		
		for j in range (self.N):
	
			r = 0.0; i = 0.0
	
			for k in range (self.N):
		
				r += self.comp[k] * cos (2.0 * pi * k * j / self.N)
				i += self.comp[k] * sin (2.0 * pi * k * j / self.N)
		
			self.inv.append ((r-i)/self.N)
		
		self.current = self.inv
		self.current_name = "fourier_inverse"
		
		return self
		
	def conv (self, v):	
			
		for i in range (self.N):
	
			r = 0
	
			for j in range (len (v.data)):
		
				if j > i: break
		
				r += self.data[i-j] * v.data[j]
	
			self.conv_t.append (r)
			
		self.current = self.conv_t
		self.current_name = "conv_time"
	
		return self

	def conv_freq (self, v):

		if hasattr (v.f, "re") and \
			hasattr (v.f, "im") and \
			hasattr (self.f, "re") and \
			hasattr (self.f, "re"): return self
	
		for a, b, c, d in zip (self.f["re"], self.f["im"], v.f["re"], v.f["im"]):

			r = a * c - b * d
			i = -a * d - b * c

			self.conv_f["re"].append (r)
			self.conv_f["im"].append (i)

			self.conv_f["comp"].append (r + i)
			self.conv_f["amp"].append (sqrt (r*r + i*i))
		
		self.comp = self.conv_f["comp"]
		self.current = self.conv_f["comp"]
		self.current_name = "conv_complex_spectre"
		
		return self
		
	def draw (self, name = None, br = False):
		
		if name is not None:
			
			if hasattr (self, name): 
		
				html.add_figure (getattr (self, name), self.name + "_" + name)
			
				if br == True: html.add_break ()		
		
		else:
			
			if self.current is not None:
			
				html.add_figure (self.current, self.name + 
												("_" if self.current_name is not "" else "") + 
												self.current_name)
			
				if br == True: html.add_break ()
		
		return self






































