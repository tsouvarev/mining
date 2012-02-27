#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp
import HTMLMaker2 as html
from Data import *
from copy import deepcopy as copy

N = 1000; L = 200
alpha = 5; f = 2; dt = 0.005

beats = {
			"200": 120, "400": 125, "600": 119, "800": 130,
			"240": -80, "440": -75, "640": -70, "840": -85
		}

u = []

# генерируем сердцебиение
for t in range (N):

	if str(t) in beats: u.append (beats [str(t)])
	else: u.append (0)

# генерируем синусоиду и дополняем ее нулями
s  = [sin (2 * pi * f * t * dt) * exp (-alpha * t * dt) for t in range (L)]
s += [0 for x in range(N-L)]

s = [i/max(s) for i in s]

u = Data (u, "heart").draw()
s = Data (s, "sin").draw()

#u.fourier ().conv_freq (s.fourier ()).fourier_inv ().draw ()
#s.fourier ().conv_freq (u.fourier ()).fourier_inv ().draw ()

g = Data ([], "inverse_filter")

alpha = 0.0000001

# находим обратный фильтр

for re, im in zip(s.fourier().f["re"], s.fourier().f["im"]):

	g.f["re"].append ( re / ( (re*re + im*im) + alpha*alpha) )
	g.f["im"].append (-im / ( (re*re + im*im) + alpha*alpha) )
	g.f["comp"].append (g.f["re"][-1] + g.f["im"][-1])
	g.f["amp"].append (sqrt (g.f["re"][-1] * g.f["re"][-1] + g.f["im"][-1]*g.f["im"][-1]))	

g.comp = g.f["comp"]

g.conv_freq (u.fourier().conv_freq(s.fourier())).fourier_inv().draw()

html.save ("./", "pics/")












#def lpf (fc):

#	dt = 0.005

##	w = new double[2*m+1]; lp (fc,m,dt,w ); fc = 10;
#	
#	m = 128;  fact = 2 * fc * dt
#	lpf = []; d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
#	
#	lpf.append (fact)
#	fact *= pi
#	
#	lpf += [sin (fact * i) / (pi * i) for i in range (1, m+1)]
#	lpf[m] /= 2
#	
#	sumg = lpf[0]; fact1 = 0; s = 0
#	
#	for i in range (1, m+1):
#	
#		s = d[0]
#		
#		for k in range (1, 4):
#		
#			s += 2.0 * d[k] * cos (pi * i * k / m)
#		
#		lpf[i] *= s
#		sumg += 2 * lpf[i]
#		
#	lpf = [lpf[i] / sumg for i in range (m+1)]
#	lpf = [lpf[- i - 1] for i in range (m)] + lpf
#	
#	return lpf

## function highpass(real[0..n] x, real dt, real RC)
##   var real[0..n] y
##   var real α := RC / (RC + dt)
##   y[0] := 0
##   for i from 1 to n
##     y[i] := α * y[i-1] + α * (x[i] - x[i-1])
##   return y

#def lab4 ():
#	
#	lp = lpf (10)
#	
#	html.add_line ()
#	html.add_figure (lp, "lpf")

#	lp_f = fourier (lp)
#	html.add_figure (lp_f["amp"], "lpf_f_amp") #  (амплитудный спектр фнч)
#	
#	s  = [sin (2 * pi * 10 * t * 0.005) +
#			sin (2 * pi * 60 * t * 0.005) +
#			sin (2 * pi * 150 * t * 0.005) for t in range (L)]
#	s += [0 for x in range(N-L)]
#	
#	html.add_figure (s, "sin")
#	
#	s_f = fourier (s)
#	s_fltr_f = conv_freq (lp_f, s_f)
#	s_fltr = fourier_inv (s_fltr_f["amp"])
#	html.add_figure (s_fltr_f["amp"], "s_fltr_f_a_amp")
#	html.add_figure (s_fltr_f["comp"], "s_fltr_f_a_comp")
#	html.add_figure (s_fltr, "s_fltr_a")
#	
#	s_fltr = fourier_inv (s_fltr_f["comp"])
#	html.add_figure (s_fltr_f["amp"], "s_fltr_f_c_amp")
#	html.add_figure (s_fltr_f["comp"], "s_fltr_f_c_comp")
#	html.add_figure (s_fltr, "s_fltr_c")
#	

##	lpf1 = lpf (10)
##	lpf2 = lpf (30)
##	
##	bpf = [a-b for (a,b) in zip (lpf1, lpf2)]
##	
##	bpf_f = fourier (bpf)
##	html.add_figure (bpf_f["amp"], "bpf_f_amp")
#	
##	lp = lpf(100)
##	hpf = [-i for i in lp]
##	
##	hpf_f = fourier (hpf)
##	html.add_figure (hpf_f["amp"], "hpf_f_amp")
	






















