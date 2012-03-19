#! /usr/bin/python
# -*- coding: utf-8 -*-

from numpy import array, zeros, empty, uint8
from os.path import basename as base
from PIL import Image

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

def hist_eq (pic, html):

	print pic

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
	
	pic = base (pic)
	
	# сохраняем новое изображение
	out.save ("pics_out/"+pic+"_res.jpg", "JPEG")

	html.add_break ()
	html.add_break ()
	html.add_picture ("pics_out/"+pic+"_res.jpg", height = '800px')	
	html.add_figure (h2, u"Гистограмма итогового изображения (%s)" %pic, height = '800px')
	html.add_figure (get_cdf (h2), u"Эквализированная гистограмма\nитогового изображения (%s)" % pic, height = '800px')
	
	html.add_break ()
	html.add_break ()
