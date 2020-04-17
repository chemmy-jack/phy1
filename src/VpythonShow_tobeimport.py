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


global keepon 
keepon = False
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
	abdomen_angle =	analyse_senior1["abdomen_angle"]
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
	scale = abs(oo_wb[-1][0]-oo_wb[0][0])/100
	print('scale', scale)
	T = len(oo_wb)
	print(T)
	cen = vector(0,0,0)

	# get coordinate data
	mid = (list2vpvec(oo_wb[0]) + list2vpvec(oo_wb[-1]))/2 # middel point, use ass offset
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

	
	# calculate mirrored wing 
	o_wt_r = [] # mirrored wing tip
	o_te_r = [] # mirrored trailing edge
	uyax = vector(0,1,0) # unit vector of y axis
	for x in range(T) :
		ta_tv = ta[x]
		ta_tv.y = 0
		wt_tv = wt[x]
		wt_tv.y = 0
		te_tv = te[x]
		te_tv.y = 0
		o_wt_r.append(o_wt[x]-2*(wt_tv-wt_tv.proj(ta_tv)))
		o_te_r.append(o_te[x]-2*(te_tv-te_tv.proj(ta_tv)))
		

	# analyse with vpython

	## abdomen angle
	abd_deg = [] # abdomen angle (degree)
	for i in range(T) :
		abd_deg.append(90-degrees(diff_angle(ta[i],uyax)))
	
	## wing norm and sw base vector 1,2 and sweeping angle
	wing_norm = [] # 翅膀法向量
	sw_base1 = [] 
	sw_base2 = []
	sw_deg = [] # sweeping angle
	for i in range(T) :
		wing_norm.append(cross(wt[i], te[i]))
		sw_base1.append(cross(wing_norm[i], ta[i]))
		sw_base2.append(rotate(sw_base1[i], pi/2, axis=wing_norm[i]))
		sw_deg.append(degrees(diff_angle(sw_base2[i], wt[i])))

	## flapping angle unit inner z axis
	uizax = []  # unit inner z axis
	flap_deg_1 = [] # flaping angle 1 (using wt vector)
	flap_deg_senior1 = [] # flapping angle senior 1 (using sw base 1)
	for i in range(T) :
		uizax.append( norm(vector(wt[i].z,0,wt[i].x)))
		ref = wt[i]
		flap_ref = ref - wt[i].proj(uizax[i])
		flap_deg_1.append(90 - degrees(diff_angle(flap_ref, ref)))
		ref = sw_base1[i]
		flap_ref = ref - wt[i].proj(uizax[i])
		flap_deg_senior1.append(90 - degrees(diff_angle(flap_ref, ref)))

	## shift angle
	direct = []
	sh_deg = []
	for i in range(T) :
		direct.append(degrees(atan(ta[i].z/ta[i].x)))
	mean_direct = mean(direct)
	for i in range(T) :
		sh_deg.append(direct[i]-mean_direct)
		

	# setup canvas and axis and center ball
	scene = canvas(title="show path "+spec_data_name, width = 1400 ,height = 800,center = cen, background = color.cyan , userspin = True, opacity = 0.2)
	xaxis = arrow(canvas = scene, pos = cen, axis = vector(1,0,0),shaftwidth = 0.01 ,color=color.blue, opacity = 0.2)
	yaxis = arrow(canvas = scene, pos = cen, axis = vector(0,1,0),shaftwidth = 0.01 ,color=color.green, opacity = 0.2)
	zaxis = arrow(canvas = scene, pos = cen, axis = vector(0,0,1),shaftwidth = 0.01 ,color=color.red, opacity = 0.2)
	cen = sphere(canvas = scene, pos = cen, radius = 0.02, opacity = 0.1)

	# setup butterfly
	wbball = sphere(canvas = scene, radius = scale, color = color.black)
	wb_trail = attach_trail(wbball, type = "points", radius = scale/2) 
	wtball = sphere(canvas = scene, radius = scale, color = color.green)
	teball = sphere(canvas = scene, radius = scale, color = color.red)
	taball = sphere(canvas = scene, radius = scale, color = color.black)
	wt_rball = sphere(canvas = scene, radius = scale, color = color.green)
	te_rball = sphere(canvas = scene, radius = scale, color = color.red)

	wingtri = triangle(
		v0 = vertex(pos = wbball.pos),
		v1 = vertex(pos = wtball.pos),
		v2 = vertex(pos = teball.pos),
		opacity = 0.5
	)
	wing_rtri = triangle(
		v0 = vertex(pos = wbball.pos),
		v1 = vertex(pos = wt_rball.pos),
		v2 = vertex(pos = te_rball.pos),
		opacity = 0.5
	)
	'''
	abd_cyl = cylinder(radius=scale/2, color = color.yellow)
	wb_wt_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_wt_r_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_te_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_te_r_cyl =  cylinder(radius=scale/2, color = color.yellow)
	'''

	# setup widgits
	def stop_func() :
		global keepon
		keepon = False
		print("stop")
		print(keepon)
	stop_but = button(bind=stop_func, text="stop all", pos=scene.caption_anchor)

	keepon = True
	dt = 0.1
	# start running visualized graph
	while keepon :
		for i in range(T):
			if keepon == False : break
			# 3D vizualize
			## points
			wbball.pos = o_wb[i]
			wtball.pos = o_wt[i]
			teball.pos = o_te[i]
			taball.pos = o_ta[i]
			te_rball.pos = o_te_r[i]
			wt_rball.pos = o_wt_r[i]
			'''
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
			'''
			## wing plate
			wingtri.v0 = vertex(pos = wbball.pos)
			wingtri.v1 = vertex(pos = wtball.pos)
			wingtri.v2 = vertex(pos = teball.pos)
			wing_rtri.v0 = vertex(pos = wbball.pos)
			wing_rtri.v1 = vertex(pos = wt_rball.pos)
			wing_rtri.v2 = vertex(pos = te_rball.pos)

			sleep(dt)

	print("finnish")
	sys.exit()
	print("finally")
	
