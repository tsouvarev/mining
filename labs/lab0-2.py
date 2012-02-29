#! /usr/bin/python
# -*- coding: utf-8 -*-

from libs.maintenance import fourier, fourier_inv, conv, conv_freq
from libs.filters import lpf, hpf, bpf, bsf
from numpy import array, zeros, append, ones, empty, concatenate, uint8
from PIL import Image
from math import sin, cos, pi, sqrt, exp, log

N = 1000; L = 200
u = zeros(N); s = zeros(N); v = array([])
alpha = 5; f = 2; dt = 0.005

re = 0; im = 1; amp = 2; comp = 3



def init ():

	global N, L, u, s, alpha, f, dt
	
	beats = {
				"200": 120, "400": 125, "600": 119, "800": 130,
				"240": -80, "440": -75, "640": -70, "840": -85
			}

	# генерируем сердцебиение
	
	for b in beats: u[int(b)] = beats[b]

	# генерируем синусоиду и дополняем ее нулями

	s[:L] = [sin (2 * pi * f * t * dt) * exp (-alpha * t * dt) for t in range (L)]

def lab0 ():

	global u, s
	
	s_f = fourier (s)
	
	html.add_figure (s, u"Синусоида")
	
	html.add_figure (s_f[:, comp], u"Комплексный спектр синусоиды")
	s_inv = fourier_inv (s_f[:, comp])
	html.add_figure (s_inv, u"Обратное преобразование Фурье для синусоиды")
	html.add_break ()

def lab1 ():
	
	global u, s
	
	s = s/max(s)
	
	# свертка кардиограммы и синусоиды	
	v = conv (u, s)

	html.add_figure (u, u"Функция давления") #  ()
	html.add_figure (s, u"Синусоида") #  (синусоида)
	html.add_figure (v, u"Результат свертки во временной области") #  ()
	html.add_break ()
	html.add_line ()
	
def lab2():

	global u, s
	
	# прямое преобразование фурье
	u_fourier = fourier (u)
	s_fourier = fourier (s)

	# свертка в частотной области
	v_freq = conv_freq (u_fourier, s_fourier)
	
	# обратное преобразование результатов свертки
	v = fourier_inv (v_freq[:,comp])
	
	html.add_figure (s_fourier[:,comp], u"Комплексный спектр Фурье для синусоиды")
	html.add_figure (v, u"Обратное преобразование свертки")
	
	html.add_break ()
	html.add_line ()
