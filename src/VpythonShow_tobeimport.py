
from vpython import *
import json as js
import jack_functions as func
import sys
import numpy as np

global keepon 
keepon = False
def VpythonShow(o_co, spec_data_name) :
	# path showing
	o_wb = o_co["wb"]
	o_wt = o_co["wt"]
	o_te = o_co["te"]
	o_ta = o_co["ta"]

	# get analyse1 data
	analyse1 = func.analyse1(o_co)

	scale = abs(o_wb[-1][0]-o_wb[0][0])/100
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

	wingtri = triangle(
		v0 = vertex(pos = wbball.pos),
		v1 = vertex(pos = wtball.pos),
		v2 = vertex(pos = teball.pos)
	)
	print(cenvec)
	abdomen_cyl = cylinder(radius=scale/2, color = color.yellow)
	wb_wt_cyl =  cylinder(radius=scale/2, color = color.yellow)
	wb_te_cyl =  cylinder(radius=scale/2, color = color.yellow)

	# setup widgits
	def stop_func() :
		global keepon
		keepon = False
		print("stop")
		print(keepon)
	stop_but = button(bind=stop_func, text="stop all", pos=scene.caption_anchor)

	# setup graph
	oscillation = graph(title="test graph", xtitle='time', ytitle='value', fast=False, width=800)
	'''
	funct1 = gcurve(color=color.blue, width=4, markers=True, marker_color=color.orange, label='curve')
	funct2 = gvbars(delta=0.4, color=color.green, label='bars')
	funct3 = gdots(color=color.red, size=6, label='dots')
	'''
	funct1 = gcurve(color=color.blue, width=2, markers=True, marker_color=color.blue, label="abdomen")
	funct2 = gcurve(color=color.red , width=2, markers=True, marker_color=color.red, label="flap")
	funct3 = gcurve(color=color.yellow , width=2, markers=True, marker_color=color.yellow, label="wingrot")
	print(scene.center)

	# plot graph
	abdomen_angle =	analyse1["abdomen_angle"]
	flapping_angle = analyse1["flapping_angle"]
	pitching_angle = analyse1["pitching_angle"]
	wingrotate_angle = analyse1["wingrotate_angle"]
	mean_direct = analyse1["mean_direct"]
	direct = analyse1["direct"]
	shift_angle = analyse1["shift_angle"]

	for time in range(T) :
		funct1.plot(time, abdomen_angle[time])
		funct2.plot(time, flapping_angle[time])
		funct3.plot(time, wingrotate_angle[time])

	# plot graph
	dt = 0.01
	keepon = True
	t = -30

	while keepon :
		print(keepon)
		for i in range(T):
			if keepon == False : break
			# 3D vizualize
			wbball.pos = vector(o_wb[i][0], -o_wb[i][1], o_wb[i][2])
			wtball.pos = vector(o_wt[i][0], -o_wt[i][1], o_wt[i][2])
			teball.pos = vector(o_te[i][0], -o_te[i][1], o_te[i][2])
			taball.pos = vector(o_ta[i][0], -o_ta[i][1], o_ta[i][2])
			abdomen_cyl.pos = wbball.pos
			abdomen_cyl.axis = taball.pos - wbball.pos
			wb_wt_cyl.pos = wbball.pos
			wb_wt_cyl.axis = wtball.pos - wbball.pos
			wb_te_cyl.pos = wbball.pos
			wb_te_cyl.axis = teball.pos - wbball.pos
			wingtri.v0 = vertex(pos = wbball.pos)
			wingtri.v1 = vertex(pos = wtball.pos)
			wingtri.v2 = vertex(pos = teball.pos)
			sleep(dt)

	print("finnish")
	sys.exit()
	print("finally")
