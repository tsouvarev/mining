#! /usr/bin/python
# -*- coding: utf-8 -*-

from math import sin, cos, pi, sqrt, exp, log
from maintenance import fourier, fourier_inv, conv, conv_freq
from maintenance_2dim import fourier_2dim#, fourier_inv_2dim
from filters import lpf, hpf, bpf, bsf #_seemed_worked
from numpy import array, zeros, append, ones, empty, concatenate, uint8
from PIL import Image
from HTMLMaker import HTMLMaker
from time import time
#import psyco

#psyco.full()
#psyco.profile()

re = 0; im = 1; amp = 2; comp = 3

html = HTMLMaker ("./", "pics/")

N = 1000; L = 200
u = zeros(N); s = zeros(N); v = array([])
alpha = 5; f = 2; dt = 0.005

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

def lab4 ():
	
	dt = 0.001
	
	lp = lpf (90, dt)
	lp_f = fourier (lp)
	
	hp = hpf (100, dt)
	hp_f = fourier (hp)

	bp = bpf (30, 100, dt)
	bp_f = fourier (bp)
	
	bs = bsf (30, 100, dt)
	bs_f = fourier (bs)
	
	s = zeros (N)
	s[:L]  = [  sin (2 * pi * 15 * t * dt) +	
				sin (2 * pi * 60 * t * dt) + 
				sin (2 * pi * 150 * t * dt) for t in range (L)]

	s_f = fourier (s)
	
	s_conv_lpf = conv (s, lp)
	s_conv_lpf_f = fourier (s_conv_lpf)

	s_conv_hpf = conv (s, hp)
	s_conv_hpf_f = fourier (s_conv_hpf)
		
	s_conv_bpf = conv (s, bp)
	s_conv_bpf_f = fourier (s_conv_bpf)
	
	s_conv_bsf = conv (s, bs)
	s_conv_bsf_f = fourier (s_conv_bsf)

	axis = [i/(dt*len(lp)) for i in range(len(lp))]

	html.add_line ()
	html.add_figure (lp, u"Фильтр низких частот")
	html.add_figure (lp_f[:,amp], u"Амплитудный спектр ФНЧ")
	html.add_figure (lp_f[:,comp], u"Комплексный спектр ФНЧ")
	html.add_break()
	
	html.add_figure (hp, u"Фильтр высоких частот")
	html.add_figure (hp_f[:,amp], u"Амплитудный спектр ФВЧ")
	html.add_figure (hp_f[:,comp], u"Комплексный спектр ФВЧ")
	html.add_break()
	
	html.add_figure (bp, u"Полосовой фильтр")
	html.add_figure (bp_f[:,amp], u"Амплитудный спектр ПФ") 
	html.add_figure (bp_f[:,comp], u"Комплексный спектр ПФ")
	html.add_break()
	
	html.add_figure (bs, u"Режекторный фильтр")
	html.add_figure (bs_f[:,amp], u"Амплитудный спектр РФ") 
	html.add_figure (bs_f[:,comp], u"Комплексный спектр РФ")
	html.add_break()

	axis = [i/(dt*len(s_f[:,amp])) for i in range(len(s_f[:,amp]))]
	html.add_figure (s, u"Полигармонический процесс")
	html.add_figure (s_f[:,amp], u"Амплитудный спектр полигармонического процесса") 
	html.add_figure (s_f[:,comp], u"Комплексный спектр полигармонического процесса")
	html.add_break()
	
	html.add_figure (s_conv_lpf, u"ПП+ФНЧ")
	html.add_figure (s_conv_lpf_f[:,amp], u"Амплитудный спектр ПП+ФНЧ") 
	html.add_figure (s_conv_lpf_f[:,comp], u"Комплексный спектр ПП+ФНЧ")
	html.add_break()
	
	html.add_figure (s_conv_hpf, u"ПП+ФВЧ")
	html.add_figure (s_conv_hpf_f[:,amp], u"Амплитудный спектр ПП+ФВЧ")
	html.add_figure (s_conv_hpf_f[:,comp], u"Комплексный спектр ПП+ФВЧ")
	html.add_break()
	
	html.add_figure (s_conv_bpf, u"ПП+ПФ")
	html.add_figure (s_conv_bpf_f[:,amp], u"Амплитудный спектр ПП+ПФ") 
	html.add_figure (s_conv_bpf_f[:,comp], u"Комплексный спектр ПП+ПФ")
	html.add_break()

	html.add_figure (s_conv_bsf, u"ПП+РФ")
	html.add_figure (s_conv_bsf_f[:,amp], u"Амплитудный спектр ПП+РФ") 
	html.add_figure (s_conv_bsf_f[:,comp], u"Комплексный спектр ПП+РФ")
	html.add_break()

def lab5 (pic, path_to_save, filter_func, f1 = None, f2 = None, suf = None):

	dx = dy = dt = 1
	fn = 1.0/(2*dx)
	fc = 0.001 # задавая частоту среза 0.001, фильтр отловит размерами 1000px и более, 0.01 – 100px, 0.1 – 10px

	i = Image.open (pic)
	pic_f = Image.new ("L", i.size)

	j = empty (i.size)
	
	if f1 == None: f = filter_func(fc)
	else:
		if f2 == None: f = filter_func(f1)
		else: f = filter_func(f1, f2)
		
	w, h = i.size
	s = 0.0; n = 0
	
	for x in range(w):
		for y in range (h):
		
			r, g, b = i.getpixel ((x,y))
			j[x][y] = 0.3*r + 0.59*g + 0.11*b

	for x in range (w):
		for y in range (h): 
			pic_f.putpixel ((x,y), j[x][y])
			
	pic_f.save (path_to_save + "/bw_" + pic, "JPEG")

	j -= j.sum()/j.size

	for x in range (w): j[x] = conv (j[x], f) # горизонтальная фильтрация
	
	for y in range (h): j[:,y] = conv (j[:,y], f) # вертикальная фильтрация	
			
	c_min = j.min(); c_max = j.max()
	
	for x in range (w):
		for y in range (h): 
		
			j[x][y] = int( (j[x][y] - c_min) * 255 / (c_max - c_min) )
			pic_f.putpixel ((x,y), j[x][y])
	
	pic_f.save (path_to_save + "/filtered_" + str(suf) + "_" + pic, "JPEG")
	
	html.add_picture (path_to_save + "/bw_" + pic)
	html.add_picture (path_to_save + "/filtered_" + str(suf) + "_" + pic)
	html.add_break ()

def gomomorf (pic, path, filter_func, f1 = None, f2 = None, suf = None):

	dx = dy = dt = 1
	fn = 1.0/(2*dx)
	fc = 0.001 # задавая частоту среза 0.001, фильтр отловит размерами 1000px и более, 0.01 – 100px, 0.1 – 10px

	i = Image.open (pic)
	pic_f = Image.new ("L", i.size)
	
	w, h = i.size
	
	j = empty ((w,h,4))	 #[[0 for y in range(h)] for x in range(w)]#
	
	if f1 == None: f = filter_func(fc)
	else:
		if f2 == None: f = filter_func(f1)
		else: f = filter_func(f1, f2)
	
	for x in range(w):
		for y in range (h):
		
			c = i.getpixel ((x,y)) + 1
			j[x,y,re] = log (c)
			#r, g, b = i.getpixel ((x,y))
			#j[x][y] = log(0.3*r + 0.59*g + 0.11*b)

#	for x in range (w):
#		for y in range (h): 
#			pic_f.putpixel ((x,y), j[x][y])
	
	#pic_f.save (path + "/bw_" + str(suf) + "_" + pic, "JPEG")

	f_f = fourier (f, max(w,h))
		
	t = time ()
	
	for x in range (w): j[x] = fourier (j[x, :, re])
	for y in range (h): j[:, y] = fourier (j[:, y, comp])
	
	print time () - t

	t = time ()
	
	for x in range (w): j[x] = conv_freq (j[x], f_f)
	for y in range (h): j[:, y] = conv_freq (j[:, y], f_f)
	
	print time () - t
	
	t = time ()
	
	for x in range (w): j[x, :, re] = fourier_inv (j[x, :, comp])
	for y in range (h): j[:, y, re] = fourier_inv (j[:, y, re])
	
	print time () - t
	
	for x in range (w): 
		for y in range (h): 
		
			j[x, y, re] = exp(j[x, y, re])-1
			
	for x in range (w):
		for y in range (h): 
			pic_f.putpixel ((x,y), j[x, y, re])
	
	pic_f.save (path + "/" + str(suf) + "_" + pic, "JPEG")
	
	html.add_picture (pic)
	html.add_picture (path + "/" + str(suf) + "_" + pic)
	html.add_break ()

def get_hist (im_p, (w,h)):

	new = zeros ((w,h), dtype=uint8)
	hist = zeros (256)
	
	# заполняем массив пикселями начального изображения
	for x in range (w):

		for y in range (h):

	#		если пиксель представлено одним числом, то это ч/б изображение
	#		и можно его брать прям так
			if type (im_p[x,y]) not in [list, tuple]: 
		
				new[x,y] = im_p [x,y]
		
	#		если пиксель представлен тремя числами и они одинаковые, то это
	#		тоже ч/б изображение и можно брать любое из них	
			elif len (im_p[x,y]) == 3 and im_p[x,y][0] == im_p[x,y][1] == im_p[x,y][2]: 
		
				new[x,y] = im_p [x,y][0]
		
	#		остался вариант, когда имеем цветное изображение с тремя каналами;
	#		используем магию вуду и преобразовываем его в ч/б
			else:
		
				r,g,b = im_p[x,y]
				new[x,y] = int (0.3 * r + 0.59 * g + 0.11 * b)
		
	#		сразу считаем гистограмму: сколько пикселей на каждом уровне яркости
			hist[ new[x,y] ] += 1
			
	return new, hist

def get_cdf (hist):

	return array ([sum (hist[:i]) for i in range (256)])

def hist_eq (pic):

	# открываем картинку
	im = Image.open (pic)
	
	html.add_picture (pic, height = '800px')

	# выделяем память под новое изображение
	out = Image.new ("L", im.size)
	w, h = im.size

	# массив пикселей начального изображения
	new = zeros (im.size, dtype=uint8)
	# гистограмма
	hist = zeros (256)
	# таблица преобразования
	trans = zeros (256)

	# получаем объекты для удобного доступа к пикселям
	im_p = im.load()
	out_p = out.load()

	new, hist = get_hist (im_p, im.size)
	
	# таблица трансформации
	trans = get_cdf (hist)

	html.add_figure (hist, u"Гистограмма (%s)" % pic, height = '800px')
	html.add_figure (trans, u"Эквализированная гистограмма (%s)" % pic, height = '800px')
	
	trans *= 255. / (h*w)
	
	# преобразовываем пиксели начального изображения
	for x in range (w):

		for y in range (h):
		
			out_p[x,y] = trans[new[x,y]] #/ (h * w)
	
	a, h2 = get_hist (out_p, im.size)
	# сохраняем новое изображение
	out.save ("pics/"+pic+"_res.jpg", "JPEG")

	html.add_break ()
	html.add_break ()
	html.add_picture ("pics/"+pic+"_res.jpg", height = '800px')	
	html.add_figure (h2, u"Гистограмма итогового изображения (%s)" %pic, height = '800px')
	html.add_figure (get_cdf (h2), u"Эквализированная гистограмма\nитогового изображения (%s)" % pic, height = '800px')
	
	html.add_break ()
	html.add_break ()

t0 = time()

#init ()
#lab0 ()
#lab1 ()
#lab2 ()
#lab3 ()
#lab4 ()

#hist_eq ("XRx1024.jpg")
#hist_eq ("XR.jpg")
hist_eq ("b.jpg")

#t = time()
#lab5 ("pic2.jpg", ".", lpf, 0.01, suf = "lpf")
#print time()-t

#t = time()
#lab5 ("pic3.jpg", "pics", hpf, 0.1, suf = "hpf")
#print time()-t

#lab5 ("pic2.jpg", "pics", bpf, 0.01, 0.05)

#t = time()
#lab5 ("pic3.jpg", ".", bpf, 0.001, 0.3, "bpf")
#print time()-t

#t = time()
#lab5 ("pic3.jpg", ".", bsf, 0.001, 0.3, "bsf")
#print time()-t

#bp = bpf (0.1, 0.01, 1)
#	
#html.add_figure (bp, u"Полосовой фильтр")

#gomomorf ("bw_pic3.jpg", "pics", lpf, 0.29, suf = "gomo")


print time() - t0

html.save ()



























