from vpython import *
import json as js
import jack_functions as func
import sys

print("getting data from ../db/rawtopside.json")
print("reminder: run this scipt in code directory, and check if rawtopside.json is in ../db")
with open ("../db/rawtopside.json", "r") as database:
    data = js.loads(database.read())
print("finnish reading data")

n = 1
# print possibles
for x in data :
	key1_1 = list(data[x].keys())[0]
	key1_1_1 = list(data[x][key1_1].keys())[0]
	nrows = len(data[x][key1_1][key1_1_1])
	print("{:2} {:3} ".format(n,nrows),x)
	n += 1

n -= 1

# choose specfic
N = input("type number of file to see track: ")
try :
	N = int(N)
except ValueError :
	print("not integer")
	sys.exit()
if N <= 0 or N > n :
	print("error: no such file")
	sys.exit()
for x in data :
	N -= 1
	if N == 0 :
		spec_data = data[x]
		print(x)
		break
o_co = func.cal_origin_coordinate(spec_data)

o_wb = o_co["wb"]
o_wt = o_co["wt"]
o_te = o_co["te"]
o_ta = o_co["ta"]

scale = abs(o_wb[-1][0]-o_wb[0][0])/100
T = len(o_wb)
print(T)
cenvec = vector((o_wb[-1][0]+o_wb[0][0])/2,(o_wb[-1][1]+o_wb[0][1])/2,(o_wb[-1][2]+o_wb[0][2])/2)
print(cenvec)

scene = canvas(title="show path "+x, width = 1400 ,height = 800,center = cenvec, background = color.cyan , userspin = True)
xaxis = arrow(canvas = scene, pos = cenvec, axis = vector(1,0,0),shaftwidth = 0.05 ,color=color.blue)
yaxis = arrow(canvas = scene, pos = cenvec, axis = vector(0,1,0),shaftwidth = 0.05 ,color=color.green)
zaxis = arrow(canvas = scene, pos = cenvec, axis = vector(0,0,1),shaftwidth = 0.05 ,color=color.red)
cen = sphere(canvas = scene, pos = cenvec, radius = 0.05)
wbball = sphere(canvas = scene, radius = scale, color = color.black)
wb_trail = attach_trail(wbball, type = "points", radius = scale/2)
wtball = sphere(canvas = scene, radius = scale, color = color.green)
# wt_trail = attach_trail(wtball, type = "points", radius = scale)
teball = sphere(canvas = scene, radius = scale, color = color.red)
# te_trail = attach_trail(teball, type = "points", radius = scale)
taball = sphere(canvas = scene, radius = scale, color = color.black)
# ta_trail = attach_trail(taball, type = "points", radius = scale)
scene.center=vector((o_wb[-1][0]+o_wb[0][0])/2,(o_wb[-1][1]+o_wb[0][1])/2,(o_wb[-1][2]+o_wb[0][2])/2)
print(cenvec)
abdomen_cyl = cylinder(radius=scale/2, color = color.yellow)
wb_wt_cyl =  cylinder(radius=scale/2, color = color.yellow)
wb_te_cyl =  cylinder(radius=scale/2, color = color.yellow)
print(scene.center)
while True :
	for i in range(T):
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
		sleep(0.1)
	
