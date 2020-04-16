
from vpython import *
import json as js
import jack_functions as func
import sys
import numpy as np

global keepon 
keepon = False
def VpythonShow(origin_coordinate, spec_data_name) :
	# path showing
	o_wb = origin_coordinate["wb"]
	o_wt = origin_coordinate["wt"]
	o_te = origin_coordinate["te"]
	o_ta = origin_coordinate["ta"]

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
		v2 = vertex(pos = teball.pos),
		opacity = 0.5
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

	for time in range(T) :
		linesen1_abdomen.plot(time, abdomen_angle[time])
		linesen1_flap.plot(time, flapping_angle[time])
		linesen1_sweeping.plot(time, sweeping_angle[time])
	# plot graph
	dt = 0.01
	keepon = True
	t = -30

	while keepon :
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
