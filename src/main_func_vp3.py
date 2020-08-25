from vpython import *
from jack_functions import get_Jsonrawdb, cal_origin_coordinate, ChooseOneWithNum
from statistics import mean


keepon = False
show_refvec = True
blaftimg = True
clones = {}
clonesw = {}
CurrentData = ''
o_wb = []
o_wt = []
o_te = []
o_ta = []
wt = []
te = []
ta = []
o_wt_r = []
o_te_r = []
T = 0
time = 0
origin_coordinate = {}
spec_data_name = ''
print("because this is a different scipt, you have to choose the database you want again. The previous choise is abondoned")
iswhat = ChooseOneWithNum(["butterfly", "ornithopter"])
databasejs = get_Jsonrawdb(iswhat)
scale = 1
# set butterfly clones
cloneops = 0.1
cloneopsw = 0.3
clonesw = {}
clonen = 10
clones = {}

cen = vector(0,0,0)

# starts here

# create objects and canvas

## setup canvas 
background_color_raw = vector(255, 253, 191)
background_color = background_color_raw/255
print('back color', background_color)
scene = canvas( width = 1400 ,height = 750,center = cen, background = background_color, userspin = True)

## setup butterfly ball
wbball = sphere(canvas = scene, radius = scale*2, color = color.red)
wtball = sphere(canvas = scene, radius = scale/2, color = color.orange)
teball = sphere(canvas = scene, radius = scale/2, color = color.purple)
taball = sphere(canvas = scene, radius = scale*2, color = color.red)
wt_rball = sphere(canvas = scene, radius = scale/2, color = color.red)
te_rball = sphere(canvas = scene, radius = scale/2, color = color.purple)

## setup butterfly cylinder
cylrad = scale/2
abd_cyl = cylinder(radius=scale*2, color = color.gray(0.5), opacity = 0.5)
wb_wt_cyl = cylinder(radius=cylrad, color = color.blue, opacity = 0.3)
wb_wt_r_cyl = cylinder(radius=cylrad, color = color.green, opacity = 0.3)
wb_te_cyl = cylinder(radius=cylrad, color = color.purple, opacity = 0.3)
wb_te_r_cyl = cylinder(radius=cylrad, color = color.purple, opacity = 0.3)

# create butterfly wing
wing_opacity = 0.75
wingtri = triangle(
	v0 = vertex(pos = cen, opacity = wing_opacity),
	v1 = vertex(pos = cen, opacity = wing_opacity),
	v2 = vertex(pos = cen, opacity = wing_opacity)
)
wing_rtri = triangle(
	v0 = vertex(pos = cen, opacity = wing_opacity),
	v1 = vertex(pos = cen, opacity = wing_opacity),
	v2 = vertex(pos = cen, opacity = wing_opacity)
)



## define update after image (clones)
def afterimgfunc() :
	global clones
	global clonesw
	i = time
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

# define initialize

def killaftimg() :
	global clones, clonesw
	for i in clones :
		for j in clones[i] :
			j.visible = False
			del j
	for i in clonesw :
		for j in clonesw[i] :
			j.visible = False
			del j
	clones = {}
	clonesw = {}

def list2vpvec(array) :
	return vector(array[0], array[1], array[2])

def GetMeanList(veclist) :
	tempx = []
	tempy = []
	tempz = []
	for i in range(T) :
		tempx.append(veclist[i][0])
		tempy.append(veclist[i][1])
		tempz.append(veclist[i][2])
	tempx = mean(tempx)
	tempy = mean(tempy)
	tempz = mean(tempz)
	mid = [tempx,tempy,tempz]
	return mid

def initialize() :
	global CurrentData
	global keepon
	global o_wb, o_wt, o_te, o_ta, wt, te, ta, o_wt_r, o_te_r, o_ta_r, time, T, keepon, iswhat
	# check the slelected 
	m = DataMenu
	print(m.selected, m.index)
	if m.selected == "blank" :
		keepon = False
		return
	if CurrentData == m.selected :
		return

	#initial quantities
	time = 0
	keepon = False
	cen = vector(0,0,0)
	o_wb = []
	o_wt = []
	o_te = []
	o_ta = []
	wt = []
	te = []
	ta = []
	o_wt_r = []
	o_te_r = []
	o_wt_r = [] # mirrored wing tip origin coordinate
	o_te_r = [] # mirrored trailing edge origin coordinate
	wt_r = [] # mirrored wing tip
	te_r = [] # mirrored trailing edge

	# update new capacities
	spec_data = databasejs[m.selected]
	origin_coordinate = cal_origin_coordinate(spec_data, iswhat)
	oo_wb = origin_coordinate["wb"]
	oo_wt = origin_coordinate["wt"]
	oo_te = origin_coordinate["te"]
	oo_ta = origin_coordinate["ta"]
	T = 100000000
	for i in origin_coordinate :
		temp = len(origin_coordinate[i]) 
		if temp<T :
			T = temp
	print('T is:', T) # updata T

	# calculate coordinate offset
	mid = list2vpvec(GetMeanList(oo_wb))
	for i in range(T) :
		o_wb.append(list2vpvec(oo_wb[i])-mid)
		o_wt.append(list2vpvec(oo_wt[i])-mid)
		o_te.append(list2vpvec(oo_te[i])-mid)
		o_ta.append(list2vpvec(oo_ta[i])-mid)
		wt.append(o_wt[i]-o_wb[i])
		te.append(o_te[i]-o_wb[i])
		ta.append(o_ta[i]-o_wb[i])
	
	# calculate mirrored wing 
	uyax = vector(0,1,0) # unit vector of y axis
	for i in range(T) :
		ta_tv = vector(ta[i].x, 0, ta[i].z)
		wt_tv = vector(wt[i].x, 0, wt[i].z)
		te_tv = vector(te[i].x, 0, te[i].z)
		o_wt_r.append(o_wt[i]-2*(wt_tv-wt_tv.proj(ta_tv)))
		o_te_r.append(o_te[i]-2*(te_tv-te_tv.proj(ta_tv)))
		wt_r.append(o_wt_r[i]-o_wb[i])
		te_r.append(o_te_r[i]-o_wb[i])

	scene.title="show path "+m.selected+", T="+str(T)
	scene.title += ', clonen= ' + str(clonen)
	CurrentData = m.selected
	scale = mag(wt[0])/30
	print('scale', scale)

	# update objects in canvas
	##set up axis and center ball 
	xaxis = arrow(canvas = scene, pos = cen, axis = vector(1,0,0)*scale,shaftwidth = 0.01 ,color=color.blue, opacity = 0.2)
	yaxis = arrow(canvas = scene, pos = cen, axis = vector(0,1,0)*scale,shaftwidth = 0.01 ,color=color.green, opacity = 0.2)
	zaxis = arrow(canvas = scene, pos = cen, axis = vector(0,0,1)*scale,shaftwidth = 0.01 ,color=color.red, opacity = 0.2)
	cen = sphere(canvas = scene, pos = cen, radius = 0.02, opacity = 0.1)

	## setup butterfly ball
	wbball = sphere(canvas = scene, radius = scale*2, color = color.red)
	wtball = sphere(canvas = scene, radius = scale/2, color = color.orange)
	teball = sphere(canvas = scene, radius = scale/2, color = color.purple)
	taball = sphere(canvas = scene, radius = scale*2, color = color.red)
	wt_rball = sphere(canvas = scene, radius = scale/2, color = color.red)
	te_rball = sphere(canvas = scene, radius = scale/2, color = color.purple)

	## setup butterfly cylinder
	cylrad = scale/2
	abd_cyl = cylinder(radius=scale*2, color = color.gray(0.5), opacity = 0.5)
	wb_wt_cyl = cylinder(radius=cylrad, color = color.blue, opacity = 0.3)
	wb_wt_r_cyl = cylinder(radius=cylrad, color = color.green, opacity = 0.3)
	wb_te_cyl = cylinder(radius=cylrad, color = color.purple, opacity = 0.3)
	wb_te_r_cyl = cylinder(radius=cylrad, color = color.purple, opacity = 0.3)

	# kill old tracks
	killaftimg()

	print("the initialize function have been activated")
	keepon = True # start the update process

# define update

def update() :
	global o_wb, o_wt, o_te, o_ta, wt, te, ta, o_wt_r, o_te_r, o_ta_r, time
	wtime.text = str("{:04d} secs".format(time))
	# 3D vizualize
	## points
	wbball.pos = o_wb[time]
	wtball.pos = o_wt[time]
	teball.pos = o_te[time]
	taball.pos = o_ta[time]
	te_rball.pos = o_te_r[time]
	wt_rball.pos = o_wt_r[time]
	## cylenders
	abd_cyl.pos = wbball.pos
	abd_cyl.axis = ta[time]
	wb_wt_cyl.pos = wbball.pos
	wb_wt_cyl.axis = wt[time]
	wb_wt_r_cyl.pos = wbball.pos
	wb_wt_r_cyl.axis = wt_rball.pos - wbball.pos
	wb_te_cyl.pos = wbball.pos
	wb_te_cyl.axis = te[time]
	wb_te_r_cyl.pos = wbball.pos
	wb_te_r_cyl.axis = te_rball.pos - wbball.pos
	
	## wing plate
	wingtri.v0.pos = wbball.pos
	wingtri.v1.pos = wtball.pos
	wingtri.v2.pos = teball.pos
	wing_rtri.v0.pos = wbball.pos
	wing_rtri.v1.pos = wt_rball.pos
	wing_rtri.v2.pos = te_rball.pos

# create widgets and define the functions of widgets
MenuList = ["blank"] + list(databasejs.keys())
DataMenu = menu(choices = MenuList, bind = initialize, position = scene.title_anchor)
wtime = wtext(text="time")


## the start button
def stpa_func() :
	global keepon
	# keepon = not keepon
	if DataMenu.selected == "blank" :
		keepon = False
		return
	keepon = True
	print("stpa", keepon)
stpa_but = button(bind=stpa_func, text="start/pause", pos=scene.caption_anchor)


# while loop starts

dt = 0.02
# start running visualized graph

while True :
	sleep(dt)
	if keepon :
		update()
		afterimgfunc()
		time += 1
		if time >= T :
			time = 0







'''


# below, is the old things

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

'''
