#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
from multiprocessing import Pool
from maintenance import fourier, fourier_inv

#def fourier_2dim (data):
#	
#	M = len (data)
#	N = len (data[0])
#	
#	re = []; im = []; amp = []; comp = []

#	for u in range (M):
#	
#		re.append ([])
#		im.append ([])
#		amp.append ([])
#		comp.append ([])
#	
#		for v in range (N):
#		
#			r = i = am = c = 0.0
#			
#			for x in range (M):
#			
#				for y in range (N):
#				
#					r += data[x][y] * (cos (2.0*pi*u*x/M) * cos (2.0*pi*v*y/N) +
#										sin (2.0*pi*u*x/M) * sin (2.0*pi*v*y/N))
#					i -= data[x][y] * (cos (2.0*pi*u*x/M) * sin (2.0*pi*v*y/N) +
#										sin (2.0*pi*u*x/M) * cos (2.0*pi*v*y/N))
#			re[-1].append (r)
#			im[-1].append (i)
#			amp[-1].append (r+i)
#			comp[-1].append (r*r + i*i)
#	
#	return {
#			"re": re, 
#			"im": im, 
#			"amp": amp, 
#			"comp": comp
#			}
	
#def fourier_inv_2dim (data):
#	
#	v = []

#	M = len (data)
#	N = len (data[0])
#	
#	for x in range (M):
#	
#		v.append ([])
#	
#		for y in range (N):
#		
#			r = i = am = c = 0.0
#			
#			for u in range (M):
#			
#				for v in range (N):
#				
#					r += data[x][y] * (cos (2.0*pi*u*x/M) * cos (2.0*pi*v*y/N) +
#										sin (2.0*pi*u*x/M) * sin (2.0*pi*v*y/N))
#					i += data[x][y] * (sin (2.0*pi*u*x/M) * cos (2.0*pi*v*y/N) +
#										cos (2.0*pi*u*x/M) * sin (2.0*pi*v*y/N))
#			
#			v[-1].append ((r-i)/N)
#			
#	return v		
			
#	for x in range(N):
#	
#		r = 0.0; i = 0.0
#		N = len (s)

#		for k in range (N):

#			r += s[k] * cos (2.0 * pi * k * j / N)
#			i += s[k] * sin (2.0 * pi * k * j / N)

#		v.append ((r-i)/N)

#	return v

def fourier_2dim (data):

	M = len (data)
	N = len (data[0])
	
	v = [0]*M
	
	for x in range (M):
	
		v[x] = (fourier(data[x])["comp"]) # ПФ по горизонтали
	
	for y in range (N):
	
		d = []
		for x in range (M): d.append (v[x][y])
		
		print len(d)
		
		d = fourier (d)["comp"]
		
		print x,y, len(v),len(v[x]), len(d)
		
		for x in range (M): v[x][y] = d[x]
	
	return v	

def conv (u, s):

	N = len (u)
	L = len (s)
	
	v = [0]*(N+L-1)
	
	for i in range (N):
	
		for j in range (L):
		
			v[i+j] += u[i] * s[j]
	
	skip = 0 if N==L else L/2
	
	return v[skip:][:N]

def conv_freq (i, j):

	re = []; im = []; comp = []; amp = []
	N = len (i["re"])
	
	for a, b, c, d in zip (i["re"], i["im"], j["re"], j["im"]):

		re.append ( a * c - b * d)
		im.append ( -a * d - b * c)

		comp.append (re[-1] + im[-1])
		amp.append (sqrt (re[-1]*re[-1] + im[-1]*im[-1]))
		
	return {
			"re": re, 
			"im": im, 
			"amp": amp, 
			"comp": comp
			}
