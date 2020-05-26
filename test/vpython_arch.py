from vpython import *

R = 19				   #球半徑 2 m

scene = canvas(align='left',width=1200, height=600, background=vector(0.7,0.9,0.9), center=vector(0,0,0),range=30, fov=pi*0.05)#設定畫面

circle_board = [vec(-R * cos(theta), R *sin(theta),0 ) for theta in arange(-pi/5, pi/5, 0.1)] #畫球面鏡

a4 = extrusion(
	pos = vec(0,0,0),
	path=circle_board,
	color=color.orange,
	shape=[ shapes.rectangle(width=1, height=2)]
)

vec1 = arrow(
	pos = vec(0,0,0),
	color = color.blue,
	axis = vec(30,0,0)
)

vec2 = arrow(
	pos = vec(0,0,0),
	color = color.red,
	axis = vec(0,30,0)
)

arch = extrusion(
	pos = vec(0,0,0),
	path=[rotate(vec1.axis, angle=theta, axis=vec(0,0,1)) for theta in arange(0,pi/2, 0.01)] ,
	color=color.orange,
	shape=[ shapes.rectangle(width=1, height=2)]
)

sphere(radius=1, pos = arch.pos, color=color.green)

cr = shapes.circle(
	radius=20,
	angle1=0,
	angle2=pi/2
	)

ar = shapes.arc(radius=20, angle1=0, angle2=pi/2)
arx = extrusion(
	pos = vec(0,0,0),
	path=[vec(0,0,0), vec(2,0,0)] ,
	color=color.black,
	shape=ar
)
carx = sphere(pos=arx.pos, radius=3, color=color.black)


ball1 = sphere(pos=vec(10,10,10), radius=3, color=color.yellow)
ball2 = sphere(pos=vec(-10,10,10), radius=3, color=color.yellow)
cball = compound([ball1,ball2])
ccall = sphere(pos=cball.pos, radius=3, color=color.purple)


