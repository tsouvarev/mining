#! /usr/bin/python
# -*- coding: utf8 -*-

from PIL import Image
from numpy import empty, zeros, array

# открываем картинку
im = Image.open ("XR.jpg")

# выделяем память под новое изображение
out = Image.new ("L", im.size)
w, h = im.size

# массив пикселей начального изображения
new = zeros (im.size)
# гистограмма
hist = zeros (256)
# таблица преобразования
trans = zeros (256)

# получаем объекты для удобного доступа к пикселям
im_p = im.load()
out_p = out.load()

# заполняем массив пикселями начального изображения
for x in range (w):

	for y in range (h):

#		если пиксель представлено одним числом, то это ч/б изображение
#		и можно его брать прям так
		if type (im_p[x,y]) is not list and type (im_p[x,y]) is not tuple: 
		
			new[x,y] = im_p [x,y]
		
#		если пиксель представлен тремя числами и они одинаковые, то это
#		тоже ч/б изображение и можно брать любое из них	
		elif len (im_p[x,y]) == 3 and im_p[x,y][0] == im_p[x,y][1] == im_p[x,y][2]: 
		
			new[x,y] = im_p [x,y][0]
		
#		остался вариант, когда имеем цветное изображение с тремя каналами;
#		используем магию вуду и преобразовываем его в ч/б
		else:
		
			r,g,b = im_p[x,y]
			new[x,y] = 0.3 * r + 0.59 * g + 0.11 * b
		
#		сразу считаем гистограмму: сколько пикселей на каждом уровне яркости
		hist[ int(new[x,y]) ] += 1

# таблица трансформации
trans = array ([sum (hist[:i]) for i in range (256)])

# преобразовываем пиксели начального изображения
for x in range (w):

	for y in range (h):
		
		out_p[x,y] = 255. * trans[int (new[x,y])] / (h * w)

# сохраняем новое изображение
out.save ("res.jpg", "JPEG")

















