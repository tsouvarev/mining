#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
from numpy import array, zeros, append, concatenate, empty
from itertools import izip_longest
from multiprocessing import Pool

re = 0; im = 1; amp = 2; comp = 3; en = 4

def fourier_part ((s,j)):
	
	r = i = am = c = 0.0
	
	N = len (s)
	for k in range (N):
	
		r += s[k] * cos (2.0 * pi * k * j / N)
		i += s[k] * sin (2.0 * pi * k * j / N)

	am = sqrt (r*r + i*i)
	c = r - i
	en = r*r + i*i

	return r,i,am,c,en

def fourier (data, l = None):
	
	if l == None:
		N = len (data)
		return array (Pool().map (fourier_part, [(data,x) for x in range(N)]))
	else:
		return array (Pool().map (fourier_part, [(data,x) for x in range(l)]))
		
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
	
	v = zeros (N+L-1)
	
	for i in range (N):
	
		for j in range (L):
		
			v[i+j] += u[i] * s[j]
	
#	skip = L/2 if N==L else 0
	skip = 0 if N==L else L/2
	return v[skip:][:N]

def conv_freq (i, j):

	v = empty ((0,4))
		
	for a, b, c, d in izip_longest (i[:,re], i[:,im], j[:,re], j[:,im], fillvalue = 0):
#	zip (i[:,re], i[:,im], j[:,re], j[:,im]):

		m =  a * c - b * d
		n = -a * d - b * c

		v = concatenate ((v, [[m, n, sqrt (m*m+n*n), m+n]]))
		
	return v[:len(i)]
	
def autocorrelation (x):

	N = len (x)
	r_xx = zeros (N)
	
	for i in range (N):
	
		for t in range (i, N):
		
			r_xx[i] += x[t] * x[t-i]
			
	return r_xx
	
def maximum (x, l=None, r=None):

	N = len (x)
	m = []
	if l is None: l = 1
	if r is None: r = N-1	
	
	for i in range (l, r):
	
		if x[i-1] < x[i] > x[i+1]: m.append ((x[i], i,))
		
	return m
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
