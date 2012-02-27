#! /usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread
from math import sin, cos, pi, sqrt, exp
from time import time
from copy import deepcopy as cp
from multiprocessing import Pool, Process, Array
from functools import partial, wraps

from HTMLMaker import HTMLMaker

html = HTMLMaker ("./", "./")

def conv_part ((u, s, v, i)):

	res = [0]*(L)

	for j in range (L):
		
		res[j] += u[i] * s[j]
		
	return res

def conv (u, s):
	
	N = len (u)
	L = len (s)

	v = [0]*(N+L-1)
	i = 0
	
	for r in Pool().map (conv_part, [(u, s, v, x) for x in range(N)]):
	
		for j in range (len(r)):
			
			v[i+j] += r[j]

		i += 1
	
	return (v[0:N] if N==L else v[L/2-1:-L/2])
	
def conv_long (u, s):
	
	N = len (u)
	L = len (s)

	v = [0]*(N+L-1)
	i = 0
	
	for i in range (N):
	
		for j in range (L):
		
			v[i+j] += u[i] * s[j]
	
	return (v[0:N] if N==L else v[L/2-1:-L/2])

N = 1000; L = 200
u = []; s = []; v = []
alpha = 5; f = 2; dt = 0.005

s  = [sin (2 * pi * f * t * dt) * exp (-alpha * t * dt) for t in range (L)]
s += [0 for x in range(N-L)]

beats = {
			"200": 120, "400": 125, "600": 119, "800": 130,
			"240": -80, "440": -75, "640": -70, "840": -85
		}

u = []

# генерируем сердцебиение

for t in range (N):

	if str(t) in beats: u.append (beats [str(t)])
	else: u.append (0)

t = time()

conv_long (u,s)

print time()-t

t = time()

conv (u,s)

print time()-t


































