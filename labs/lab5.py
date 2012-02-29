#! /usr/bin/python
# -*- coding: utf-8 -*-

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


