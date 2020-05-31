from vpython import *
import json as js
import jack_functions as func
import sys
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
clones = {}
clonesw = {}

def VpythonShow(origin_coordinate, spec_data_name) :
	# path showing
	o_wb = origin_coordinate["wb"]
	o_wt = origin_coordinate["wt"]
	o_te = origin_coordinate["te"]
	o_ta = origin_coordinate["ta"]

	scale = abs(o_wb[-1][0]-o_wb[0][0])/100
	print('scale', scale)
	T = len(o_wb)
	print(T)
	# cenvec = vector((o_wb[-1][0]+o_wb[0][0])/2,-(o_wb[-1][1]+o_wb[0][1])/2,(o_wb[-1][2]+o_wb[0][2])/2)
	cenvec = vector(0,0,0)
	cenarray = np.array([(o_wb[-1][0]+o_wb[0][0])/2,(o_wb[-1][1]+o_wb[0][1])/2,(o_wb[-1][2]+o_wb[0][2])/2])
	print(cenvec)
	for x in range(T) :
		o_wb[x] = np.subtract(o_wb[x], cenarray)
		o_wt[x] = np.subtract(o_wt[x], cenarray)
		o_te[x] = np.subtract(o_te[x], cenarray)
		o_ta[x] = np.subtract(o_ta[x], cenarray)
	
	
	# calculate mirrored wing
	o_wt_a = []
	o_te_a = []
	for x in range(T) :
		o_wb_tv = np.array([o_wb[x][0], o_wb[x][2]]) # top view coordinate x,y
		o_ta_tv = np.array([o_ta[x][0], o_ta[x][2]]) # top view coordinate x,y
		o_te_tv = np.array([o_te[x][0], o_te[x][2]]) # top view coordinate x,y
		o_wt_tv = np.array([o_wt[x][0], o_wt[x][2]]) # top view coordinate x,y
		o_wt_tv = (GetMirrorDot(o_wb_tv,o_ta_tv,o_wt_tv))# top view coordinate x,y of wing tip mirrored
		o_te_tv = (GetMirrorDot(o_wb_tv,o_ta_tv,o_te_tv))# top view coordinate x,y of trainling edge mirrored
		o_te_a.append([o_te_tv[0], o_te[x][1], o_te_tv[1]])
		o_wt_a.append([o_wt_tv[0], o_wt[x][1], o_wt_tv[1]])

	# setup canvas and axis and center ball
	scene = canvas(title="show path "+spec_data_name, width = 1400 ,height = 800,center = cenvec, background = color.cyan , userspin = True, opacity = 0.2)
	xaxis = arrow(canvas = scene, pos = cenvec, axis = vector(1,0,0),shaftwidth = 0.01 ,color=color.blue, opacity = 0.2)
	yaxis = arrow(canvas = scene, pos = cenvec, axis = vector(0,1,0),shaftwidth = 0.01 ,color=color.green, opacity = 0.2)
	zaxis = arrow(canvas = scene, pos = cenvec, axis = vector(0,0,1),shaftwidth = 0.01 ,color=color.red, opacity = 0.2)
	cen = sphere(canvas = scene, pos = cenvec, radius = 0.02, opacity = 0.1)

	# setup butterfly
	wbball = sphere(canvas = scene, radius = scale, color = color.black)
	wb_trail = attach_trail(wbball, type = "points", radius = scale/2) 
	wtball = sphere(canvas = scene, radius = scale, color = color.green)
	# wt_trail = attach_trail(wtball, type = "points", radius = scale)
	teball = sphere(canvas = scene, radius = scale, color = color.red)
	# te_trail = attach_trail(teball, type = "points", radius = scale)
	taball = sphere(canvas = scene, radius = scale, color = color.black)
	# ta_trail = attach_trail(taball, type = "points", radius = scale)
	# scene.center=vector((o_wb[-1][0]+o_wb[0][0])/2,(o_wb[-1][1]+o_wb[0][1])/2,(o_wb[-1][2]+o_wb[0][2])/2)
	wt_aball = sphere(canvas = scene, radius = scale, color = color.green)
	te_aball = sphere(canvas = scene, radius = scale, color = color.red)

	wingtri = triangle(
		v0 = vertex(pos = wbball.pos),
		v1 = vertex(pos = wtball.pos),
		v2 = vertex(pos = teball.pos),
		opacity = 0.5
	)
	wing_atri = triangle(
		v0 = vertex(pos = wbball.pos),
		v1 = vertex(pos = wt_aball.pos),
		v2 = vertex(pos = te_aball.pos),
		opacity = 0.5
	)
	print(cenvec)
	abdomen_cyl = cylinder(radius=scale/2, color = color.yellow)
	wb_wt_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_wt_a_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_te_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_te_a_cyl =  cylinder(radius=scale/2, color = color.yellow)

	# setup widgits
	def stop_func() :
		global keepon
		keepon = False
		print("stop")
		print(keepon)
	stop_but = button(bind=stop_func, text="stop all", pos=scene.caption_anchor)
#	def storerawdata_func() :
		
	# get analyse1 data
	analyse1 = func.analyse1(origin_coordinate)

	# get analyse_senior1 data
	analyse_senior1 = func.analyse_senior1(origin_coordinate)

	# setup graph
	## analyse1
	graph_analyse1 = graph(title="analyse1", xtitle='time', ytitle='value', fast=False, width=800)
	line1_abdomen = gcurve(graph=graph_analyse1, color=color.blue, width=2, markers=True, marker_color=color.blue, label="abdomen")
	line1_flap = gcurve(graph=graph_analyse1, color=color.red , width=2, markers=True, marker_color=color.red, label="flap")
	line1_wingrotate = gcurve(graph=graph_analyse1, color=color.yellow , width=2, markers=True, marker_color=color.yellow, label="wingrot")
	line1_directshift = gcurve(graph=graph_analyse1, color=color.green , width=2, markers=True, marker_color=color.green, label="directshift")
	## analyse_senior1
	graph_analyse_senior1 = graph(title="analyse_senior1", xtitle='time', ytitle='value', fast=False, width=800)
	linesen1_abdomen = gcurve(graph=graph_analyse_senior1, color=color.blue, width=2, markers=True, marker_color=color.blue, label="abdomen")
	linesen1_flap = gcurve(graph=graph_analyse_senior1, color=color.red , width=2, markers=True, marker_color=color.red, label="flap")
	linesen1_sweeping = gcurve(graph=graph_analyse_senior1, color=color.orange , width=2, markers=True, marker_color=color.orange, label="sweeping")

	# plot graph
	## analyse1
	abdomen_angle =	analyse1["abdomen_angle"]
	flapping_angle = analyse1["flapping_angle"]
	pitching_angle = analyse1["pitching_angle"]
	wingrotate_angle = analyse1["wingrotate_angle"]
	mean_direct = analyse1["mean_direct"]
	direct = analyse1["direct"]
	shift_angle = analyse1["shift_angle"]

	for time in range(T) :
		line1_abdomen.plot(time, abdomen_angle[time])
		line1_flap.plot(time, flapping_angle[time])
		line1_wingrotate.plot(time, wingrotate_angle[time])
		line1_directshift.plot(time, shift_angle[time])
	## analyse_senior1
	abdomen_angle = analyse_senior1["abdomen_angle"]
	flapping_angle = analyse_senior1["flapping_angle"]
	sweeping_angle = analyse_senior1["sweeping_angle"]
	reference_vector = analyse_senior1["reference_vector"]
	unit_sw_base_vector = analyse_senior1["unit_sw_base_vector"]
	reference_vector2 = analyse_senior1["reference_vector2"]
	unit_body_right_ve = analyse_senior1["unit_body_right_vec"]

	for time in range(T) :
		linesen1_abdomen.plot(time, abdomen_angle[time])
		linesen1_flap.plot(time, flapping_angle[time])
		linesen1_sweeping.plot(time, sweeping_angle[time])
	# plot graph
	dt = 0.01
	keepon = True

	# reference vector
	reference_cyl =  cylinder(radius=scale/2, color = color.black)
	reference_cyl2 =  cylinder(radius=scale/2, color = color.black)
	
	while keepon :
		for i in range(T):
			if keepon == False : break
			# 3D vizualize
			## points
			wbball.pos = vector(o_wb[i][0], o_wb[i][1], o_wb[i][2])
			wtball.pos = vector(o_wt[i][0], o_wt[i][1], o_wt[i][2])
			teball.pos = vector(o_te[i][0], o_te[i][1], o_te[i][2])
			taball.pos = vector(o_ta[i][0], o_ta[i][1], o_ta[i][2])
			te_aball.pos = vector(o_te_a[i][0], o_te_a[i][1], o_te_a[i][2])
			wt_aball.pos = vector(o_wt_a[i][0], o_wt_a[i][1], o_wt_a[i][2])
			## cylenders
			abdomen_cyl.pos = wbball.pos
			abdomen_cyl.axis = taball.pos - wbball.pos
			wb_wt_cyl.pos = wbball.pos
			wb_wt_cyl.axis = wtball.pos - wbball.pos
			wb_wt_a_cyl.pos = wbball.pos
			wb_wt_a_cyl.axis = wt_aball.pos - wbball.pos
			wb_te_cyl.pos = wbball.pos
			wb_te_cyl.axis = teball.pos - wbball.pos
			wb_te_a_cyl.pos = wbball.pos
			wb_te_a_cyl.axis = te_aball.pos - wbball.pos
			## wing plate
			wingtri.v0 = vertex(pos = wbball.pos)
			wingtri.v1 = vertex(pos = wtball.pos)
			wingtri.v2 = vertex(pos = teball.pos)
			wing_atri.v0 = vertex(pos = wbball.pos)
			wing_atri.v1 = vertex(pos = wt_aball.pos)
			wing_atri.v2 = vertex(pos = te_aball.pos)

			reference_cyl.pos = vector(o_wb[i][0], o_wb[i][1], o_wb[i][2])
			reference_cyl.axis = vector(reference_vector[i][0] * scale*50  , -reference_vector[i][1] * scale*50  , reference_vector[i][2] * scale*50  )
			reference_cyl.pos = vector(o_wb[i][0], o_wb[i][1], o_wb[i][2])
			reference_cyl.axis = vector(reference_vector[i][0] * scale*50  , -reference_vector[i][1] * scale*50  , reference_vector[i][2] * scale*50  )

			sleep(dt)

	print("finnish")
	sys.exit()
	print("finally")

def list2vpvec(array) :
	return vector(array[0], array[1], array[2])

def VpythonShow2(origin_coordinate, spec_data_name) :
	oo_wb = origin_coordinate["wb"]
	oo_wt = origin_coordinate["wt"]
	oo_te = origin_coordinate["te"]
	oo_ta = origin_coordinate["ta"]
	T = 100000000
	for i in origin_coordinate :
		temp = len(origin_coordinate[i]) 
		if temp<T :
			T = temp
	print(T)
	cen = vector(0,0,0)

	# get coordinate data
	mid = (list2vpvec(oo_wb[0]) + list2vpvec(oo_wb[-1]))/2 # middle point, use ass offset
	o_wb = []
	o_wt = []
	o_te = []
	o_ta = []
	wt = []
	te = []
	ta = []
	for i in range(T) :
		o_wb.append(list2vpvec(oo_wb[i])-mid)
		o_wt.append(list2vpvec(oo_wt[i])-mid)
		o_te.append(list2vpvec(oo_te[i])-mid)
		o_ta.append(list2vpvec(oo_ta[i])-mid)
		wt.append(o_wt[i]-o_wb[i])
		te.append(o_te[i]-o_wb[i])
		ta.append(o_ta[i]-o_wb[i])
	
	scale = mag(wt[0])/30
#	scale = abs(oo_wb[-1][0]-oo_wb[0][0])/100
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
		

	# analyse with vpython

	## abdomen angle
	abd_deg = [] # abdomen angle (degree)
	for i in range(T) :
		abd_deg.append(90-degrees(diff_angle(ta[i],uyax)))
	
	## dwt 
	dwt = []
	diffn = 2
	for i in range(diffn) : dwt.append(wt[i+diffn]-wt[i])
	for i in range(diffn,T-diffn) : dwt.append(wt[i+diffn]-wt[i-diffn])
	for i in range(diffn) : dwt.append(wt[i]-wt[i-diffn])

	## wing norm and sw base vector 1,2 and sweeping angle and wing rotate angle of analyse 1 
	wing_norm = [] # 翅膀法向量
	sw_base1 = [] 
	sw_base2 = []
	sw_deg = [] # sweeping angle
	wrot_deg = [] # wing rotation of analyse 1 according to the pitching axis

	for i in range(T) :
		wing_norm.append(cross(wt[i], te[i]))
		sw_base1.append(cross(wing_norm[i], ta[i]))
		sw_base2.append(rotate(sw_base1[i], pi/2, axis=wing_norm[i]))
		sw_deg.append(90-degrees(diff_angle(sw_base2[i], wt[i])))
		wrot_deg.append(degrees(diff_angle(dwt[i], te[i]-te[i].proj(wt[i])))-90)

	## flapping angle unit inner z axis
	izax = []  # inner z axis
	flap_deg_1 = [] # flaping angle 1 (using wt vector)
	flap_deg_s1 = [] # flapping angle senior 1 (using sw base 1)
	for i in range(T) :
		izax.append( vector(ta[i].z,0,-ta[i].x))
		ref = wt[i]
		flap_ref = ref - ref.proj(izax[i])
		flap_ref.y = abs(flap_ref.y)
		flap_deg_1.append(90 - degrees(diff_angle(flap_ref, ref)))
		ref = sw_base1[i]
		flap_ref = ref - ref.proj(izax[i])
		flap_ref.y = abs(flap_ref.y)
		flap_deg_s1.append(degrees(diff_angle(flap_ref, ref))-90)

	## pitching angle in analyse 1
	pi1 = [] # in analyse 1, pitching axis uses the axis of wing flapping 
	pi1_deg = []
	for i in range(T) :
		pi1.append(cross(dwt[i], izax[i]))
		pi1_deg.append(90-degrees(diff_angle(pi1[i], uyax))) # method should be same as abdomen angles
	
	## shift angle
	direct = []
	sh_deg = []
	for i in range(T) :
		direct.append(degrees(atan(ta[i].z/ta[i].x)))
	mean_direct = mean(direct)
	for i in range(T) :
		sh_deg.append(direct[i]-mean_direct)

	# unitilize vectors (for better visualization)
	for i in range(T) :
		wing_norm[i] = wing_norm[i].norm() * scale * 10
		sw_base1[i] = sw_base1[i].norm() * scale * 10
		sw_base2[i] = sw_base2[i].norm() * scale * 10
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
	sw_base1_cyl = cylinder(radius=refcylrad, color = color.purple, opacity = refcylopc)
	sw_base2_cyl = cylinder(radius=refcylrad, color = color.red, opacity = refcylopc)
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
			sw_base1_cyl.pos = wbball.pos
			sw_base2_cyl.pos = wbball.pos
			izax_cyl.pos = wbball.pos
			dwt_cyl.pos = wtball.pos
			pi1_cyl.pos = wbball.pos

			wing_norm_cyl.axis = wing_norm[ts.value]
			sw_base1_cyl.axis = sw_base1[ts.value]
			sw_base2_cyl.axis = sw_base2[ts.value]
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
			sw_base1_cyl.opacity = 0.0
			sw_base2_cyl.opacity = 0.0
			izax_cyl.opacity = 0.0
			show_refvec = False
		elif b.checked :
			dwt_cyl.opacity = refcylopc
			pi1_cyl.opacity = refcylopc
			wing_norm_cyl.opacity = refcylopc
			sw_base1_cyl.opacity = refcylopc
			sw_base2_cyl.opacity = refcylopc
			izax_cyl.opacity = refcylopc
			show_refvec = True
		update()
	refvecshow_but = checkbox(bind=refvecshow_func, text="show refence vector",checked=True)
	refvecshow_but.checked = False
	refvecshow_func()


#	def cleartrail_func() :
#		wb_trail.clear()
#		wb_trail.start()
#		wb_trail.stop()
#	cleartrail_but = button(bind=cleartrail_func, text='clear wb trail', pos= scene.caption_anchor)


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
	#	ad += 'aaa'
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

	
	scene.append_to_caption('\n')
	wdata = wtext(text='')

	# setup graph 
	graph_analyse = graph(title="analyse", xtitle='time', ytitle='value', fast=False, width=1200, height=800)
	l_abd_deg = gcurve(graph=graph_analyse, color=color.blue, width=2, markers=True, marker_color=color.blue, label="abd_deg")
	l_pi1_deg = gcurve(graph=graph_analyse, color=color.green, width=2, markers=True, marker_color=color.green, label="pi1_deg")
	l_sw_deg = gcurve(graph=graph_analyse, color=color.green, width=2, markers=True, marker_color=color.green, label="sw_deg")
	l_sh_deg = gcurve(graph=graph_analyse, color=color.red, width=2, markers=True, marker_color=color.red, label="sh_deg")
	l_flap_deg_s1 = gcurve(graph=graph_analyse, color=color.cyan, width=2, markers=True, marker_color=color.cyan, label="flap_deg_s1")
	l_flap_deg_1 = gcurve(graph=graph_analyse, color=color.purple, width=2, markers=True, marker_color=color.purple, label="flap_deg_1")
	l_wrot_deg = gcurve(graph=graph_analyse, color=color.black, width=2, markers=True, marker_color=color.black, label="wrot_deg")


	# plot graph
	for time in range(T) :
		l_abd_deg.plot(time, abd_deg[time])
		l_pi1_deg.plot(time, pi1_deg[time])
		l_sw_deg.plot(time, sw_deg[time])
		l_sh_deg.plot(time, sh_deg[time])
		l_flap_deg_1.plot(time, flap_deg_1[time])
		l_flap_deg_s1.plot(time, flap_deg_s1[time])
		l_wrot_deg.plot(time, wrot_deg[time])



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

def Deletejsonraw(data) :
	spec_data_name = func.GetSpecKeyByNum(data)

	print("are u sure you want to delete", func.bcolors.WARNING, spec_data_name,func.bcolors.ENDC, "?(yes to confirm)", end = " ")

	if input() == "yes" :	
		data.pop(spec_data_name, None)
		print("new key db keys:")
		func.PrintKeysWithNum(data)
		func.write_Jsondb(data)
		print("db modified")
	else : print("nothing is changed")

