#! /usr/bin/python
# -*- coding: utf-8 -*-

def lab3():
	
	global u, s
	
	v_fourier = fourier (conv (u, s))
	s_fourier = fourier (s)
#	re = array([]); im = array([]); amp = array([]); comp = array([])
	alpha = 0.001
	g = empty ((0,4))
	
	# находим обратный фильтр
	for r, i in zip(s_fourier[:,re], s_fourier[:,im]):

		m = r / ( r*r + i*i + alpha*alpha ) 
		n = -i / ( r*r + i*i + alpha*alpha ) 
		g = concatenate ((g, [[m, n, sqrt (m*m + n*n), m + n]]))
	
	html.add_figure (fourier_inv (g[:,comp]), u"Обратный фильтр во временной области") #  ()
	html.add_figure (g[:,comp], u"Комплексный спектр для обратного фильтра") #  ()
	html.add_figure (g[:,amp], u"Амлитудный спектр для обратного фильтра") #  ()
	html.add_break ()
	
	# находим оценку исходной функции
	u_est = conv_freq (g, v_fourier)
		
	# переводим во временную область
	u = fourier_inv (u_est[:,comp])
	html.add_figure (u, u"Оценка функции давления") #  ()
	
	html.add_break ()
