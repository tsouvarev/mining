#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
from numpy import array, zeros, append, delete

def lpf (fc, dt = None, L = None, m = None, truncate = False):

	if dt == None: dt = 1
	if m == None: m = 32

	if fc >= 1/(2.0*dt): 
	
		if truncate == False: raise Exception ("fc > 1/2dt!!")		
		else: fc = 1/(2.0*dt)
	
	if fc < 0: 
	
		if truncate == False: raise Exception ("fc < 0")		
		else: fc = 0.00001

	
	fact = 2 * fc * dt
	lpf = array([fact]); d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
	
	fact *= pi
	
	lpf = append (lpf, [sin (fact * i) / (pi * i) for i in range (1, m+1)])
	
	lpf[m] /= 2.0
		
	for i in range (1, m+1):
	
		s = d[0]
		
		for k in range (1, 4):
		
			s += 2.0 * d[k] * cos (pi * i * k / m)

		lpf[i] *= s
		
	lpf /= lpf[0] + 2.0 * sum(lpf[1:])

	lpf = append (lpf[::-1][:m], lpf)
	
	if L is not None: lpf = append (lpf, zeros (L-m))
	
	return lpf

def hpf (fc, dt = None, L = None, m = None, truncate = False):

	f = -1 * lpf (fc, dt, L, m, truncate)
	f[ len (f) / 2 ] = 1 + f[ len(f) / 2 ]
	
	return f
	
def bpf (fc1, fc2, dt = None, L = None, m = None, truncate = False):

	lpf1 = lpf (fc1, dt, L, m, truncate)
	lpf2 = lpf (fc2, dt, L, m, truncate)
	
	return lpf2 - lpf1

def bsf (fc1, fc2, dt = None, L = None, m = None, truncate = False):

	lpf1 = lpf (fc1, dt, L, m, truncate)
	lpf2 = lpf (fc2, dt, L, m, truncate)

	f = lpf1 - lpf2
	f[ len (f) / 2 ] = 1 + lpf1[ len (lpf1) / 2 ] - lpf2[ len (lpf2) / 2 ]
	
	return f

