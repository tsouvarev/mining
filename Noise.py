#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp, log
from maintenance import fourier, fourier_inv, conv, conv_freq
from filters import lpf, hpf, bpf, bsf
from Generators import * 
from numpy import array, zeros, append, ones, empty, concatenate, copy
from HTMLMaker import HTMLMaker
from time import time
from random import uniform, gauss, SystemRandom, random
import psyco


psyco.full()
psyco.profile()

re = 0; im = 1; amp = 2; comp = 3; en = 4

html = HTMLMaker ("./", "pics/")

N = 1000; L = 200
u = zeros(N); s = zeros(N); v = array([])
alpha = 5; f = 2; dt = 0.005

def inf():
  i = 1
  while True:
      yield i
      i += 1

def linear_trend (a, dx, b, n):
	
	return array ([a*x+b for x in range (n)])

def exp_trend (a, b, n):
	
	return array ([a*exp(b*x) for x in range (n)])

def add_spikes (l, r, n, d):
	
	v = copy (d)
	
	for i in range (n):
	
		rand = uniform (l,r)
		x = int (random ()*len (d))
		
		v[x] += rand
	
	return v
	
def add_trend (t, d):

	v = copy (d) + t

	return v

def get_stats (data):

	avg_sq = dev = mean = sko = 0.0
	
	mean = sum(data) / len(data)
	avg_sq = sum (map (lambda x: x*x, data)) / len(data)
	dev = sum (map (lambda x: (x-mean)**2, data)) / len(data)
	sko = sqrt (dev)

	return {
			"mean": mean,
			"avg_sq": avg_sq,
			"dev": dev,
			"sko": sko
			}

#  Оценка влияния различных шумов на операцию деконволюции при решении обратных задач
#численного моделирования процессов (описать и сделать приложение для демонстрации трех
#конструкций обратных фильтров: 1 - идеального G=1/H в отсутствие шумов, 2 -
#регуляризированного G=H*/(|H|^2 +a^2) в присутствие белого шума, 3 - Винеровского типа
#G=H*/(|H|^2 +b|N|^2) в присутствие белого и узкополосного шума в виде полигармонического
#процесса для восстановления формы функции давления из модельной кардиограммы).


def reverse_filter (d, t = "ideal", N = None, v = None):

	d_f = fourier (d)
	g = empty ((0,4))

	if t == "ideal": 
	
		a = 0.00001
		
		for r, i in zip(d_f[:,re], d_f[:,im]):

			#m = 1 / (r+a if r != 0 else 1500)
			#n = 1 / (i+a if i != 0 else 1500)
			m = r / (r*r+i*i)
			n = -i / (r*r+i*i)
			
			g = concatenate ((g, [[m, n, sqrt (m*m + n*n), m + n]]))		
	
	elif t == "regular": 
	
		alpha = 0.4
	
		# находим обратный фильтр
		for r, i in zip(d_f[:,re], d_f[:,im]):

			m = r / ( r*r + i*i + alpha*alpha ) 
			n = -i / ( r*r + i*i + alpha*alpha ) 
			g = concatenate ((g, [[m, n, sqrt (m*m + n*n), m + n]]))
					
	elif t == "viner":
	
		if N == None or v == None: return None
	
		N = fourier (N)
		v = fourier (v)
	
		# находим обратный фильтр
		for r, i, n_r, n_i, v_r, v_i in zip(d_f[:,re], d_f[:,im], N[:,re], N[:,im], v[:,re], v[:,im]):
		
			b = 1/(v_r*v_r + v_i*v_i)
			
			n_n = n_r*n_r + n_i*n_i

			m = r / ( r*r + i*i + b*n_n ) 
			n = -i / ( r*r + i*i + b*n_n ) 
			
			g = concatenate ((g, [[m, n, sqrt (m*m + n*n), m + n]]))	
	
#	print g
	
	return g

def init ():

	#x = array ([2*(gauss(0,1)-0.5) for i in range (N)])
	u = zeros(N); s = zeros(N); v = array([])
	beats = {
				"200": 120, "400": 125, "600": 119, "800": 130,
				"240": -80, "440": -75, "640": -70, "840": -85
			}

	# генерируем сердцебиение
	
	for b in beats: u[int(b)] = beats[b]

	# генерируем синусоиду и дополняем ее нулями

	d = zeros (N)	
#	d[:L] = [sin (2 * pi * f * t * 0.008) * exp (-alpha * t * 0.008) for t in range (L)]
	dt = 1; m = 64; n = 10


	d  = [  sin (2 * pi * 1 * t * 0.008 + 10*pi) 
#			+ sin (2 * pi * 17 * t * 0.008) 
#			+ sin (2 * pi * 150 * t * 0.008) 
			for t in range (N)]
			
	a = array ([lfsr().next() for i in range (N)])*5
	a_f = fourier (a)
	bpf_f = fourier (bpf (0.1, 0.2, L = N, m = m))
	a_short_f = conv_freq (a_f, bpf_f)
	a_short = fourier_inv (a_short_f[:,comp])
	
	#d_n = conv (d, a_short)
#	
	html.add_figure (d, u"Синусоида")
#	html.add_figure (add_spikes (-1, 1, 30, d), u"Синусоида с импульсами")
#	html.add_figure (add_trend (linear_trend (0.001, 0.01, 2, len(d)), d), u"Синусоида с линейным трендом")
#	html.add_figure (add_trend (exp_trend (0.001, 0.01, len(d)), d), u"Синусоида с экспоненциальным трендом")

	html.add_break ()		
	
	d = zeros (N)
	d[:L] = [sin (2 * pi * f * t * 0.008) * exp (-alpha * t * 0.008) for t in range (L)]
	
	v = conv (u,d)
	v_n = v + a
	
	html.add_figure (u, u"Кардиограмма")
#	html.add_figure (d, u"Синусоида")
	html.add_figure (v, u"Свертка")
	html.add_figure (v_n, u"Свертка с шумом")
	
	v_f = fourier (v)
	v_n_f = fourier (v_n)

	d_f = fourier (d)
	
#	g_i = reverse_filter (d, "ideal", a, v)
	g_r = reverse_filter (d, "regular", a, v)
#	g_v = reverse_filter (d+a, "viner", a, v)
	
#	html.add_figure (g_i[:,comp], u"Обратный идеальный фильтр\n(комплексный спектр)")
	html.add_figure (g_r[:,comp], u"Обратный регулярный фильтр\n(комплексный спектр)")
#	html.add_figure (g_v[:,comp], u"Обратный винеровский фильтр\n(комплексный спектр)")
#	
#	g_f = conv_freq (g_i, v_f)
#	d_est = fourier_inv (g_f[:,comp])
#	html.add_figure (d_est, u"Деконволюция идеальным фильтром")
	
	g_f = conv_freq (g_r, v_f)
	d_est = fourier_inv (g_f[:,comp])
	html.add_figure (d_est, u"Деконволюция регулярным фильтром")
	
#	g_f = conv_freq (g_v, v_n_f)
#	d_est = fourier_inv (g_f[:,comp])
#	html.add_figure (d_est, u"Деконволюция винеровским фильтром")
	
#	print d_est

#	html.add_figure (d_est, u"Синусоида inv")

#	generators = [	(lfsr, 		u"Регистр сдвига с линейной обратной связью"), 
#					(congruous, u"Конгруэнтный генератор"), 
#					(swbg, 		u"Фибоначчи с запаздываниями")]
#	
#	for gen, title in generators:
#	
#		a = array ([gen().next() for i in range (N)])
#		
#		a_f = fourier (a)
#		bpf_f = fourier (bpf (0.1, 0.2, L = N, m = m))
#		a_short_f = conv_freq (a_f, bpf_f)
#		a_short = fourier_inv (a_short_f[:,comp])
#		
#		html.add_figure (a, title)
#		html.add_figure (a_short, title + u" \n(узкополосный шум)")
#		html.add_break ()
#		html.add_figure (a_f[:, comp], title + u" \n(комплексный спектр)", dt = 1)
#		html.add_figure (a_f[:, amp], title + u" \n(амплитудный спектр)", dt = 1)
#		html.add_break ()
#		html.add_figure (a_short_f[:,comp], title + u" \n(комплексный спектр узкополосного шума)", dt = 1)
#		html.add_figure (a_short_f[:,amp], title + u" \n(амплитудный спектр узкополосного шума)", dt = 1)
#		html.add_break ()
#		
#		r = get_stats (a)
#		html.add_table ([	["Среднее", round (r["mean"], n)],
#							["Дисперсия", round (r["dev"], n)],
#							["Cредне-квадратическое<br>отклонение", round (r["sko"], n)]
#						], u"Широкополосный шум")
#								
#		r = get_stats (a_short)
#		html.add_table ([	["Среднее", round (r["mean"], n)],
#							["Дисперсия", round (r["dev"], n)],
#							["Cредне-квадратическое<br>отклонение", round (r["sko"], n)]
#						], u"Узкополосный шум")
#		html.add_clear ()
#		html.add_break ()

t0 = time()

init ()

print time() - t0

html.save ()



























