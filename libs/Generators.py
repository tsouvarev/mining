#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
from numpy import array, zeros, append, concatenate, empty
from itertools import izip_longest
from multiprocessing import Pool
from random import random

def congruous ():

	beta = 19837
	seed = round (random() * 1000000)
	mod = 2 ** 16
	prev = seed % mod
	
	while (True):
		
		prev = (beta * prev) % mod
		yield (prev / mod)

def swbg ():

	a, b = 97, 33
	m = max(a,b)
	k = m-1
	
	x = array ([congruous().next() for i in range (m)])
	
	while (True):
	
		xka = x[m + k - a if k < a else k-a]
		xkb = x[m + k - b if k < b else k-b]
		res = xka - xkb
		
		if xka < xkb: res += 1
		
		x[k] = res
		k = k+1 if k+1 < m else 0
		
		yield abs (res)

def lfsr ():

	mask = 0x80000057
	n = 32
	sr = int (random()*1000000)
	res = 0x0
	
	while (True):
	
		for i in range (n):
		
			if sr & 0x00000001 == 0x1:
			
				sr = (sr ^ mask >> 1) | 0x80000000
				res |= 1 << i

			else:
			
				sr >>= 1
				
		yield abs ((res / (180000.0*11000)+0.22))-1
	



































