from vpython import *
import json as js
import jack_functions as func
import numpy as np
from numpy import linalg as LA
from math import cos, sin, asin, acos, tan, atan, radians, degrees, sqrt
from statistics import mean

def lineFromPoints(P,Q): 
	a = Q[1] - P[1] 
	b = P[0] - Q[0]  
	c = a*(P[0]) + b*(P[1]) 
	c = -c
	return a, b, c # ax + by + c = 0

def mirrorImage( a, b, c, x1, y1): # ax + by + c = 0  
	temp = -2 * (a * x1 + b * y1 + c) /(a * a + b * b)
	x = temp * a + x1 
	y = temp * b + y1
	return [x, y] 

def GetMirrorDot(A,B,C) : # C dot mirror refer to AB line, format: list
	aa, bb, cc = lineFromPoints(A,B)
	return mirrorImage(aa, bb, cc, C[0], C[1])


keepon = True
show_refvec = True
blaftimg = True

def list2vpvec(array) :
	return vector(array[0], array[1], array[2])

def VpythonShow2(origin_coordinate, spec_data_name) :
	oo_wb = origin_coordinate["wb"]
	oo_wt = origin_coordinate["wt"]
	oo_te = origin_coordinate["te"]
	oo_ta = origin_coordinate["ta"]
	cen = vector(0,0,0)

	# call get data function
	vadata = VpythonAnalyseSpec(origin_coordinate) # vector and analyse data
	vecdata = vadata["vectors"]

	T = vadata["T"]
	diffn = vecdata["diffn"]
	print(T)
	# get coordinate data
	mid = (list2vpvec(oo_wb[0]) + list2vpvec(oo_wb[-1]))/2 # middle point, use ass offset
	o_wb = vecdata["o_wb"]
	o_wt = vecdata["o_wt"]
	o_te = vecdata["o_te"]
	o_ta = vecdata["o_ta"]
	wt = vecdata["wt"]
	te = vecdata["te"]
	ta = vecdata["ta"]
	dwt = vecdata["dwt"]
	wing_norm = vecdata["wm"] # 翅膀法向量
	izax = vecdata["izax"]  # inner z axis
	pi1 = vecdata["pitch"] # in analyse 1, pitching axis uses the axis of wing flapping 
	# analysed
	abd_deg = vadata["abdomen angle"] # abdomen angle (degree)
	angatk_deg = vadata["angle of attack"]
	flap_deg_1 = vadata["flapping angle"] # flaping angle 1 (using wt vector)
	pi1_deg = vadata["pitching angle"]
	## shift angle
	sh_deg = vadata["shift angle"]

	scale = mag(wt[0])/30
	print('scale', scale)

	# calculate mirrored wing 
	o_wt_r = [] # mirrored wing tip origin coordinate
	o_te_r = [] # mirrored trailing edge origin coordinate
	wt_r = [] # mirrored wing tip
	te_r = [] # mirrored trailing edge
	uyax = vector(0,1,0) # unit vector of y axis
	for i in range(T) :
		ta_tv = vector(ta[i].x, 0, ta[i].z)
		wt_tv = vector(wt[i].x, 0, wt[i].z)
		te_tv = vector(te[i].x, 0, te[i].z)
		o_wt_r.append(o_wt[i]-2*(wt_tv-wt_tv.proj(ta_tv)))
		o_te_r.append(o_te[i]-2*(te_tv-te_tv.proj(ta_tv)))
		wt_r.append(o_wt_r[i]-o_wb[i])
		te_r.append(o_te_r[i]-o_wb[i])
		

	# unitilize vectors (for better visualization)
	for i in range(T) :
		wing_norm[i] = wing_norm[i].norm() * scale * 10
		dwt[i] = dwt[i] * scale
		pi1[i] = pi1[i].norm() * scale * 10
		izax[i] = izax[i].norm() * scale * 10

	# setup canvas and axis and center ball
	background_color_raw = vector(255, 253, 191)
	background_color = background_color_raw/255
	print('back color', background_color)
	scene = canvas(title="show path "+spec_data_name+", T="+str(T)+", diffn of dwt="+str(diffn), width = 1400 ,height = 750,center = cen, background = background_color, userspin = True)
	xaxis = arrow(canvas = scene, pos = cen, axis = vector(1,0,0)*scale,shaftwidth = 0.01 ,color=color.blue, opacity = 0.2)
	yaxis = arrow(canvas = scene, pos = cen, axis = vector(0,1,0)*scale,shaftwidth = 0.01 ,color=color.green, opacity = 0.2)
	zaxis = arrow(canvas = scene, pos = cen, axis = vector(0,0,1)*scale,shaftwidth = 0.01 ,color=color.red, opacity = 0.2)
	cen = sphere(canvas = scene, pos = cen, radius = 0.02, opacity = 0.1)

	# setup butterfly
	wbball = sphere(canvas = scene, radius = scale*2, color = color.red)
#	wb_trail = attach_trail(wbball, type = "points", radius = scale/3, color=color.red, opacity = 0)
	wtball = sphere(canvas = scene, radius = scale/2, color = color.orange)
#	wt_trail = attach_trail(wtball, type = "points", radius = scale/3, color=color.black)
	teball = sphere(canvas = scene, radius = scale/2, color = color.purple)
	taball = sphere(canvas = scene, radius = scale*2, color = color.red)
	wt_rball = sphere(canvas = scene, radius = scale/2, color = color.red)
	te_rball = sphere(canvas = scene, radius = scale/2, color = color.purple)

	wing_opacity = 0.75
	wingtri = triangle(
		v0 = vertex(pos = wbball.pos, opacity = wing_opacity),
		v1 = vertex(pos = wtball.pos, opacity = wing_opacity),
		v2 = vertex(pos = teball.pos, opacity = wing_opacity)
	)
	wing_rtri = triangle(
		v0 = vertex(pos = wbball.pos, opacity = wing_opacity),
		v1 = vertex(pos = wt_rball.pos, opacity = wing_opacity),
		v2 = vertex(pos = te_rball.pos, opacity = wing_opacity)
	)
	cylrad = scale/2
	abd_cyl = cylinder(radius=scale*2, color = color.gray(0.5), opacity = 0.5)
	wb_wt_cyl = cylinder(radius=cylrad, color = color.blue, opacity = 0.3)
	wb_wt_r_cyl = cylinder(radius=cylrad, color = color.green, opacity = 0.3)
	wb_te_cyl = cylinder(radius=cylrad, color = color.purple, opacity = 0.3)
	wb_te_r_cyl = cylinder(radius=cylrad, color = color.purple, opacity = 0.3)

	refcylrad = scale/4
	refcylopc = 0.3
	dwt_cyl = cylinder(radius=refcylrad, color = color.black, opacity = refcylopc)
	pi1_cyl = cylinder(radius=refcylrad, color = color.black, opacity = refcylopc)
	wing_norm_cyl = cylinder(radius=refcylrad, color = color.magenta, opacity = refcylopc)
	izax_cyl = cylinder(radius=refcylrad, color = color.black, opacity = refcylopc)

	# make time slider
	def timeslider_func(val) :
#		wb_trail.stop()
		update()
#		wb_trail.start()
	ts = slider(min = 0, max = T-1, value = 0, bind = timeslider_func, step = 1, pos=scene.caption_anchor) # time slider
	wtime = wtext(text="time")

	#define update
	def update() :
		global show_refvec
		wtime.text = str("{:04d} secs".format(ts.value))
		# 3D vizualize
		## points
		wbball.pos = o_wb[ts.value]
		wtball.pos = o_wt[ts.value]
		teball.pos = o_te[ts.value]
		taball.pos = o_ta[ts.value]
		te_rball.pos = o_te_r[ts.value]
		wt_rball.pos = o_wt_r[ts.value]
		## cylenders
		abd_cyl.pos = wbball.pos
		abd_cyl.axis = ta[ts.value]
		wb_wt_cyl.pos = wbball.pos
		wb_wt_cyl.axis = wt[ts.value]
		wb_wt_r_cyl.pos = wbball.pos
		wb_wt_r_cyl.axis = wt_rball.pos - wbball.pos
		wb_te_cyl.pos = wbball.pos
		wb_te_cyl.axis = te[ts.value]
		wb_te_r_cyl.pos = wbball.pos
		wb_te_r_cyl.axis = te_rball.pos - wbball.pos
		if show_refvec :
			wing_norm_cyl.pos = wtball.pos
			izax_cyl.pos = wbball.pos
			dwt_cyl.pos = wtball.pos
			pi1_cyl.pos = wbball.pos

			wing_norm_cyl.axis = wing_norm[ts.value]
			dwt_cyl.axis = dwt[ts.value]
			izax_cyl.axis = izax[ts.value]
			pi1_cyl.axis = pi1[ts.value]
		
		## wing plate
		wingtri.v0.pos = wbball.pos
		wingtri.v1.pos = wtball.pos
		wingtri.v2.pos = teball.pos
		wing_rtri.v0.pos = wbball.pos
		wing_rtri.v1.pos = wt_rball.pos
		wing_rtri.v2.pos = te_rball.pos
	
	# set butterfly clones
	cloneops = 0.1
	cloneopsw = 0.3
	global clonesw
	clonesw = {}
	clonen = 10
	global clones
	clones = {}
#	cloneswt = extrusion(path=o_wt, shape=shapes.circle(radius=1), color=color.red, opacity=cloneops)
	scene.title += ', clonen= ' + str(clonen)

	# define update after image function
	def afterimgfunc() :
		global clones
		global clonesw
		i = ts.value
		if i == 0 : bl = 0 
		else : bl = i%clonen
		if bl == 0 :
			if i not in clonesw :
				clones[i]=([
					wbball.clone(opacity=cloneops),
					wtball.clone(opacity=cloneops),
					teball.clone(opacity=cloneops),
					taball.clone(opacity=cloneops),
					wt_rball.clone(opacity=cloneops),
					te_rball.clone(opacity=cloneops),
					abd_cyl.clone(opacity=cloneops/2),
					wb_wt_cyl.clone(opacity=cloneops),
					wb_wt_r_cyl.clone(opacity=cloneops),
					wb_te_cyl.clone(opacity=cloneops),
					wb_te_r_cyl.clone(opacity=cloneops),
#			extrusion(path=o_wt, shape=shapes.circle(radius=1), color=color.red, opacity=cloneops)
				])
			if i not in clonesw :
				clonesw[i]=([
					triangle(
						v0 = vertex(pos = wbball.pos, opacity = cloneopsw),
						v1 = vertex(pos = wtball.pos, opacity = cloneopsw),
						v2 = vertex(pos = teball.pos, opacity = cloneopsw)
					),
					triangle(
						v0 = vertex(pos = wbball.pos, opacity = cloneopsw),
						v1 = vertex(pos = wt_rball.pos, opacity = cloneopsw),
						v2 = vertex(pos = te_rball.pos, opacity = cloneopsw)
					)
				])
		

	# setup widgits
	def stpa_func() :
		global keepon
		keepon = not keepon
		print("stpa")
	stpa_but = button(bind=stpa_func, text="start/pause", pos=scene.caption_anchor)


	midrange = 20
	def clearmid_func() :
		global clones
		global clonesw
		for i in clones :
			if i < (T/2+midrange) and i > (T/2-midrange) :
				for j in clones[i] :
					j.visible = False
		for i in clonesw :
			if i < (T/2+midrange) and i > (T/2-midrange) :
				for j in clonesw[i] :
					j.visible = False
	clearmid_but = button(bind=clearmid_func, text="clear middle", pos=scene.caption_anchor)
	scene.title += ', clear middle range: ' + str(midrange)

	'''
	def aftimgchops(goal) :
		for i in clones :
			for j in i :
				j.opacity = goal
	def aftimgchopsw(goal) :
		for i in clonesw :
			for j in i :
				j.v0.opacity = goal
				j.v1.opacity = goal
				j.v2.opacity = goal
	def aftimg() :
		global blaftimg
		b = aftimg_but
		if not b.checked :
			blaftimg = False
			aftimgchops(0)
			aftimgchopsw(0)
		if b.checked :
			blaftimg = True
			aftimgchops(cloneops)
			aftimgchopsw(cloneopsw)
		print("blaftimg")
	aftimg_but = checkbox(bind=aftimg, text="after image", pos=scene.caption_anchor, checked=True )
	aftimg_but.checked = False
	aftimg()
	def aftimgbut() :
		global clones
		global clonesw
		for i in clones :
			for j in clones[i] :
				j.visible = False
		for i in clonesw :
			for j in clonesw[i] :
				j.visible = False
	aftimg_but = button(bind=aftimgbut, text="clear after image", pos=scene.caption_anchor)
	'''

	def aftimg() :
		global blaftimg
		global clones
		global clonesw
		b = aftimg_ch
		if not b.checked :
			for i in clones :
				for j in clones[i] :
					j.visible = False
			for i in clonesw :
				for j in clonesw[i] :
					j.visible = False
		if b.checked :
			for i in clones :
				for j in clones[i] :
					j.visible = True
			for i in clonesw :
				for j in clonesw[i] :
					j.visible = True
	aftimg_ch = checkbox(bind=aftimg, text="after image", pos=scene.caption_anchor, checked=True )

	def aftimgbut() :
		global blaftimg
		global clones
		for i in clones :
			for j in clones[i] :
				del j
		for i in clonesw :
			for j in clonesw[i] :
				del j
	aftimg_but = button(bind=aftimgbut, text="delete after image", pos=scene.caption_anchor, checked=True )
	'''
	def wttrail() :
		if not b.checked :
		if b.checked :
		global blaftimg b = wttrail_but
		if not b.checked :
			wt_trail.stop()
			wt_trail.clear()
		if b.checked :
			wt_trail.start()
	wttrail_but = checkbox(bind=wttrail, text="wtip trail", pos=scene.caption_anchor, checked=True )
	'''
	def switch_fuc() :
		if graph_analyse.height == 400 :
			graph_analyse.height = 800
			scene.height = 750 
		else :
			graph_analyse.height = 400
			scene.height = 400 
	switch_but = button(bind=switch_fuc, text='switch show', pos=scene.caption_anchor)

	def toggledata_func() : 
		if wdata.text == '' :
			wdata.text = ad
		else : wdata.text = ''
	toggledata_but = button(bind=toggledata_func, text='toggle data', pos=scene.caption_anchor)

	def refvecshow_func() :
		global show_refvec
		b = refvecshow_but
		if not b.checked :
			dwt_cyl.opacity = 0.0
			pi1_cyl.opacity = 0.0
			wing_norm_cyl.opacity = 0.0
			izax_cyl.opacity = 0.0
			show_refvec = False
		elif b.checked :
			dwt_cyl.opacity = refcylopc
			pi1_cyl.opacity = refcylopc
			wing_norm_cyl.opacity = refcylopc
			izax_cyl.opacity = refcylopc
			show_refvec = True
		update()
	refvecshow_but = checkbox(bind=refvecshow_func, text="show refence vector",checked=True)
	refvecshow_but.checked = False
	refvecshow_func()

	'''
	def cleartrail_func() :
		wb_trail.clear()
		wb_trail.start()
		wb_trail.stop()
	cleartrail_but = button(bind=cleartrail_func, text='clear wb trail', pos= scene.caption_anchor)
	'''
	# print analysed data in page
	ad = "" # append data
	'''
	for i in range(T) :
		ad += '{}, '.format(abd_deg[i])
		ad += '{}, '.format(pi1_deg[i])
		ad += '{}, '.format(sw_deg[i])
		ad += '{}, '.format(sh_deg[i])
		ad += '{}, '.format(flap_deg_1[i])
		ad += '{}, '.format(flap_deg_s1[i])
		ad += '{}; '.format(wrot_deg[i])
		ad += 'aaa'
	'''
	'''
	ad += ';' + spec_data_name + ', '
	for i in range(T) : ad += '{}, '.format(i)
	ad += ';abd_deg, '
	for i in range(T) : ad += '{}, '.format(abd_deg[i])
	ad += ';pi1_deg, '
	for i in range(T) : ad += '{}, '.format(pi1_deg[i])
	ad += ';sw_deg, '
	for i in range(T) : ad += '{}, '.format(sw_deg[i])
	ad += ';sh_deg, '
	for i in range(T) : ad += '{}, '.format(sh_deg[i])
	ad += ';flap_deg_1, '
	for i in range(T) : ad += '{}, '.format(flap_deg_1[i])
	ad += ';flap_deg_s1, '
	for i in range(T) : ad += '{}, '.format(flap_deg_s1[i])
	ad += ';wrot_deg, '
	for i in range(T) : ad += '{}, '.format(wrot_deg[i])
	ad += ';(sqrt(o_wb[i].x**2+o_wb[i].z**2)), '
	for i in range(T) : ad += '{}, '.format(sqrt((o_wb[i].x-o_wb[0].x)**2+(o_wb[i].z-o_wb[0].z)**2))
	ad += ';o_wb[i].y-o_wb[0].y, '
	for i in range(T) : ad += '{}, '.format(o_wb[i].y-o_wb[0].y)
	def win_func(s) :
		print('check')
	win = winput(text=ad,bind=win_func)
	'''

	scene.append_to_caption('\n')
	wdata = wtext(text='')

	# setup graph 
	graph_analyse = graph(title="analyse", xtitle='time', ytitle='value', fast=False, width=1200, height=800)
	l_abd_deg = gcurve(graph=graph_analyse, color=color.blue, width=2, markers=True, marker_color=color.blue, label="abd_deg")
	l_pi1_deg = gcurve(graph=graph_analyse, color=color.green, width=2, markers=True, marker_color=color.green, label="pi1_deg")
	l_sh_deg = gcurve(graph=graph_analyse, color=color.red, width=2, markers=True, marker_color=color.red, label="sh_deg")
	l_flap_deg_1 = gcurve(graph=graph_analyse, color=color.purple, width=2, markers=True, marker_color=color.purple, label="flap_deg_1")
	l_angatk_deg = gcurve(graph=graph_analyse, color=color.yellow, width=2, markers=True, marker_color=color.yellow, label="angatk_deg")


	# plot graph
	for time in range(T) :
		l_abd_deg.plot(time, abd_deg[time])
		l_pi1_deg.plot(time, pi1_deg[time])
		l_sh_deg.plot(time, sh_deg[time])
		l_angatk_deg.plot(time, angatk_deg[time])
		l_flap_deg_1.plot(time, flap_deg_1[time])



	dt = 0.02
#	wb_trail.clear()
	# start running visualized graph
	while True :
		sleep(dt)
		if keepon :
			update()
#			if blaftimg :
			afterimgfunc()

			ts.value += 1
			if ts.value >= T :
				ts.value = 0
#				wb_trail.stop()
#		elif ts.value == 1 :
#				wb_trail.start()



def Deletejsonraw(data, iswhat = "don't know") :
	spec_data_name = func.GetSpecKeyByNum(data)

	print("are u sure you want to delete", func.bcolors.WARNING, spec_data_name,func.bcolors.ENDC, "?(yes to confirm)", end = " ")

	if input() == "yes" :	
		data.pop(spec_data_name, None)
		print("new key db keys:")
		func.PrintKeysWithNum(data)
		func.write_Jsondb(data, iswhat)
		print("db modified")
	else : print("nothing is changed")


def VpythonRefVector(origin_coordinate, T) : # all return in vector class
	oo_wb = origin_coordinate["wb"]
	oo_wt = origin_coordinate["wt"]
	oo_te = origin_coordinate["te"]
	oo_ta = origin_coordinate["ta"]

	# get coordinate data
	mid = (list2vpvec(oo_wb[0]) + list2vpvec(oo_wb[-1]))/2 # middle point, use ass offset
	o_wb = []
	o_wt = []
	o_te = []
	o_ta = []
	wt = []
	te = []
	ta = []
	dwt = []
	diffn = 2
	## wt, te, ta, dwt
	for i in range(T) :
		o_wb.append(list2vpvec(oo_wb[i])-mid)
		o_wt.append(list2vpvec(oo_wt[i])-mid)
		o_te.append(list2vpvec(oo_te[i])-mid)
		o_ta.append(list2vpvec(oo_ta[i])-mid)
		wt.append(o_wt[i]-o_wb[i])
		te.append(o_te[i]-o_wb[i])
		ta.append(o_ta[i]-o_wb[i])
	## dwt
	for i in range(diffn) : dwt.append(wt[i+diffn]-wt[i])
	for i in range(diffn,T-diffn) : dwt.append(wt[i+diffn]-wt[i-diffn])
	for i in range(diffn) : dwt.append(wt[i]-wt[i-diffn])
	## wing_norm
	wing_norm = [] # 翅膀法向量
	for i in range(T) :
		wing_norm.append(cross(wt[i], te[i]))

	## izax
	izax = []  # inner z axis
	for i in range(T) :
		izax.append( vector(ta[i].z,0,-ta[i].x))
	
	## pitch vec
	pitch = []
	for i in range(T) :
		pitch.append(cross(dwt[i], izax[i]))

	# return wt, te, ta,,, wing_norm, dwt, izax
	
	refdict = {
		"wt":wt,
		"te":te,
		"ta":ta,
		"wm":wing_norm,
		"izax":izax,
		"pitch":pitch,
		"o_wb":o_wb,
		"o_wt":o_wt,
		"o_te":o_te,
		"o_ta":o_ta,
		"dwt":dwt,
		"diffn":diffn
	}
	# o_wb = []
	return refdict

def VpythonAnalyseSpec(origin_coordinate, ynvec = "need vec") : # input origin coordinate, return lists of angle and qualities
	# calculate T
	T = 100000000
	for i in origin_coordinate :
		temp = len(origin_coordinate[i]) 
		if temp<T :
			T = temp
	print("T is : ", T)

	# get the reference vectors
	refvecdict = VpythonRefVector(origin_coordinate, T)
	wt = refvecdict["wt"]
	te = refvecdict["te"]
	ta = refvecdict["ta"]
	wing_norm = refvecdict["wm"]
	izax = refvecdict["izax"]
	pitch = refvecdict["pitch"]
	o_wb = refvecdict["o_wb"]
	o_wt = refvecdict["o_wt"]
	o_te = refvecdict["o_te"]
	o_ta = refvecdict["o_ta"]
	dwt = refvecdict["dwt"]
	uyax = vector(0,1,0) # unit vector of y axis

	## abdomen angle
	abd_deg = [] # abdomen angle (degree)
	for i in range(T) :
		abd_deg.append(90-degrees(diff_angle(ta[i],uyax)))

	## flapping angle
	flap_deg = [] # flaping angle 1 (using wt vector)
	for i in range(T) :
		ref = wt[i]
		flap_ref = ref - ref.proj(izax[i])
		flap_ref.y = abs(flap_ref.y)
		flap_deg.append(90 - degrees(diff_angle(flap_ref, ref)))

	## pitching angle
	pitch_deg = []
	for i in range(T) :
		pitch_deg.append(90-degrees(diff_angle(pitch[i], uyax))) # method should be same as abdomen angles

	## angle of attack
	angatk_deg = [] # wing rotation of analyse 1 according to the pitching axis
	for i in range(T) :
		angatk_deg.append(degrees(diff_angle(dwt[i], te[i]-te[i].proj(wt[i])))-90)

	## shift angle
	### calc mean path vec
	path2dvecx = []
	path2dvecz = []
	diff = 4
	for i in range(T-4) :
	    temp = o_wb[i+4] - o_wb[i]
	    path2dvecx.append(temp.x)
	    path2dvecz.append(temp.z)
	meanpathvec = vector(sum(path2dvecx),0,sum(path2dvecz)).rotate(angle=pi/2,axis=vector(0,1,0))
	direct = []
	sh_deg = []
	for i in range(T) :
	    # temp = ta[i]
	    # temp.y = 0
	    temp = vector(ta[i].x,0,ta[i].z)
	    direct.append(temp)
	    # direct.append(degrees(atan(ta[i].z/ta[i].x)))
	# mean_direct = mean(direct)
	for i in range(T) :
	    # sh_deg.append(direct[i]-mean_direct)
	    sh_deg.append(90-degrees(diff_angle(direct[i],meanpathvec)))

	## x,y
	ix = [] # inner x
	iy = [] # inner y
	for i in range(T) : 
	    ix.append(sqrt((o_wb[i].x-o_wb[0].x)**2+(o_wb[i].z-o_wb[0].z)**2))
	    iy.append(o_wb[i].y-o_wb[0].y)
	
	## vx,vy, omega
	vx = []
	vy = []
	omega = []
	difvn = 2
	dt = 0.001
	for i in range(T-difvn) :
	    vx.append((ix[i+difvn]-ix[i])/(dt*difvn))
	    vy.append((iy[i+difvn]-iy[i])/(dt*difvn))
	    omega.append((flap_deg[i+difvn]-flap_deg[i])/(dt*difvn))
	for i in (vx, vy, omega) :
	    i.insert(0,i[0])
	    i.append(i[-1])

        ## span, bdlen, wtpl(wing tip path lenth), abdomen amplitude
	span = []
	bdlen = []
	########## code missing
	for i in range(T) :
	    span.append(mag(wt[i]))
	    bdlen.append(mag(ta[i]))
	wtpl = [0]
	for i in range(T-1) :
	    thislen = mag(o_wt[i+1]-o_wt[i])
	    wtpl.append(wtpl[-1]+thislen)
	abd_amp = max(abd_deg) - min(abd_deg)
	


	# return as a dict
	#### return:  abdomen angle | flapping angle | pitching angle | angle of attack | shift angle | x | y | | |
	retdict = {
		"abdomen angle":abd_deg,
		"flapping angle":flap_deg,
		"pitching angle":pitch_deg,
		"angle of attack":angatk_deg,
		"shift angle":sh_deg,
		"x":ix,
		"y":iy,
		"vx":vx,
		"vy":vy,
		"T":T, # csv2
		"span":span,
		"body lenth":bdlen,
		"omega":omega,
		"wing tip path lenth":wtpl,
		"abdomen aplitude":abd_amp # csv2
	}
	if ynvec == "need vec" :
		retdict["vectors"] = refvecdict
	# elif ynvec == "no nedd vec" :
	return retdict

def VpythonAnalyseAll(alldata, iswhat = "don't know") : # input the whole database json
	print("vpython analyse all is running...")
	allanalysed = {}
	for dataname in alldata :
		print("calc of :", dataname, iswhat)
		origin_coordinate = func.cal_origin_coordinate(alldata[dataname], iswhat)
		allanalysed[dataname] = VpythonAnalyseSpec(origin_coordinate, "no need vec")
		# allanalysed[dataname] = origin_coordinate
		print("analysed ", dataname)
	return allanalysed

def ExportAnalysedData2CSV(andb, iswhat = "don't know") : # input the whole analzed data, export them in a formatt of csv file
	print("under here the exporting process should be running...")
	width = 16 # the number of column per data
	DataList = list(andb.keys())
	print("these are the 'analsyedall' keys:", DataList)
	print("these are the keys in first data", andb[DataList[0]].keys())
	print("the width is :", width)
	#### to see details of what under parameters mean, search the record on the exp notebook of 20202/8/24
	Tlist = []
	abd_amp_list =[]
	extitle = []
	bigT = 0
	allcolumns = 0
	excsv = ""
	coma = ","
	nextrow = "\n"
	datlen = 0
	gap = []

	mean_span = []
	mean_omega = []
	mean_bdlen = []


	datlen = len(DataList)
	for i in range(datlen) :
		nowdatname = DataList[i]
		nowdat = andb[nowdatname]
		Tlist.append(nowdat.pop("T", None))
		abd_amp_list.append(nowdat.pop("abdomen aplitude", None))
		extitle.append(list(nowdat.keys()))
		gap.append(width - len(extitle[i]) -1)
		mean_span.append(mean(nowdat["span"]))
		mean_omega.append(mean([abs(ele) for ele in nowdat["omega"]]))
		mean_bdlen.append(mean(nowdat["body lenth"]))
		
	print("Tlist", Tlist)

	allcolumns = width * datlen
	print("all columns:", allcolumns)
	
	bigT = max(Tlist)
	print("row lenth", bigT)

	for i in range(datlen) :
		title = DataList[i]
		excsv += title + coma
		for j in range(len(extitle[i])) :
			excsv += extitle[i][j] + coma
		for k in range(gap[i]) :
			excsv += coma
		
	excsv += nextrow

	for t in range(bigT) :
		for i in range(datlen) :
			if t >= Tlist[i] :
				for col in range(width) :
					excsv += coma
			else :
				time = str(t)
				excsv += time + coma
				for j in range(len(extitle[i])) :
					excsv += str(andb[DataList[i]][extitle[i][j]][t]) + coma
				for k in range(gap[i]) :
					excsv += coma
		excsv += nextrow

	# the excsv2
	excsv2 = ""
	# T, mean span, mean omega, mean body lenth, abd_amp (abdomen amplitude)
	########## code missing
	excsv2 += "data name,mspan,mbody lenth,momega,abdomen amplitude,T" + nextrow
	for i in range(datlen) :
	    excsv2 += DataList[i] + coma
	    excsv2 += str(mean_span[i]) + coma
	    excsv2 += str(mean_bdlen[i]) + coma
	    excsv2 += str(mean_omega[i]) + coma
	    excsv2 += str(abd_amp_list[i]) + coma
	    excsv2 += str(Tlist[i]) +coma
	    excsv2 += nextrow


	folderpath = func.GetFolderPath()
	func.writecsv1(excsv, folderpath)
	func.writecsv2(excsv2, folderpath)
	# print(excsv)
	print("all is well")
	return


