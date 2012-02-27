#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
from numpy import array, zeros, append
from itertools import izip_longest
from multiprocessing import Pool

def fourier_part ((s,j)):
	
	r = i = am = c = 0.0
	
	N = len (s)
	for k in range (N):
	
		r += s[k] * cos (2.0 * pi * k * j / N)
		i += s[k] * sin (2.0 * pi * k * j / N)

	am = sqrt (r*r + i*i)
	c = r - i

	return r,i,am,c

def fourier (data):
	
	N = len (data)
	re = array([]); im = array([]); amp = array([]); comp = array([])
	
	for r, i, a, c in Pool().map (fourier_part, [(data,x) for x in range(N)]):

		re = append (re, r); amp = append (amp, a)
		im = append (im, i); comp = append (comp, c)
	
	return {
			"re": re, 
			"im": im, 
			"amp": amp, 
			"comp": comp
			}

def fourier_inv_part ((s,j)):

	r = 0.0; i = 0.0
	N = len (s)
	
	for k in range (N):
	
		r += s[k] * cos (2.0 * pi * k * j / N)
		i += s[k] * sin (2.0 * pi * k * j / N)
	
	return (r-i)/N

def fourier_inv (data):
	
	N = len (data)
	return array(Pool().map (fourier_inv_part, [(data,x) for x in range(N)]))

def conv (u, s):

	N = len (u)
	L = len (s)
	
	v = zeros(N+L-1)
	
	for i in range (N):
	
		for j in range (L):
		
			v[i+j] += u[i] * s[j]
	
	skip = 0 if N==L else L/2
	
	return v[skip:][:N]

#def conv (u, s):

#	N = len (u)
#	L = len (s)
#	
#	v = [0]*(N+L-1)
#	
#	for i in range (N):
#	
#		for j in range (L):
#		
#			v[i+j] += u[i] * s[j]
#	
#	skip = 0 if N==L else L/2
#	
#	return v[skip:][:N]

def conv_freq (i, j):

	re = array([]); im = array([]); comp = array([]); amp = array([])
	N = len (i["re"])
	
	for a, b, c, d in izip_longest (i["re"], i["im"], j["re"], j["im"], fillvalue = 0):

		re = append (re,  a * c - b * d)
		im = append (im, -a * d - b * c)

		comp = append (comp, re[-1] + im[-1])
		amp = append (amp, sqrt (re[-1]*re[-1] + im[-1]*im[-1]))
		
	return {
			"re": re, 
			"im": im, 
			"amp": amp, 
			"comp": comp
			}
