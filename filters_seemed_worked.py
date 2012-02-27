#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
from multiprocessing import Pool, cpu_count
from itertools import chain
from numpy import array, zeros, append

def lpf (fc, dt = None):

	if dt == None: dt = 1
	
	m = 64;  fact = 2 * fc * dt
	lpf = []; d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
	
	lpf.append (fact)
	fact *= pi
	
	lpf += [sin (fact * i) / (pi * i) for i in range (1, m+1)]
	lpf[m] /= 2
		
	for i in range (1, m+1):
	
		s = d[0]
		
		for k in range (1, 4):
		
			s += 2.0 * d[k] * cos (pi * i * k / m)
		
		lpf[i] *= s
		
	sumg = sum(lpf)
		
	lpf = [lpf[i] / (2 * sumg) for i in range (m+1)]
	lpf = [lpf[- i - 1] for i in range (m)] + lpf
	
	return lpf

def hpf (fc, dt = None):

	f = [-i for i in lpf (fc, dt)]
	f[ len (f) / 2 ] = 1 + f[ len(f) / 2 ]
	
	return f
	
def bpf (fc1, fc2, dt = None):

	lpf1 = lpf (fc1, dt)
	lpf2 = lpf (fc2, dt)
	
	return [a - b for (a,b) in zip (lpf2, lpf1)]

def bsf (fc1, fc2, dt = None):

	lpf1 = lpf (fc1, dt)
	lpf2 = lpf (fc2, dt)

	f = [a - b for (a,b) in zip (lpf1, lpf2)]
	f[ len (f) / 2 ] = 1 + lpf1[ len (lpf1) / 2 ] - lpf2[ len (lpf2) / 2 ]
	
	return f

