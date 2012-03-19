#! /usr/bin/python
# -*- coding: utf-8 -*-

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
