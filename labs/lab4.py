#! /usr/bin/python
# -*- coding: utf-8 -*-

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
