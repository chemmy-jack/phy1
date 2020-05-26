import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
import jack_functions as func
import math as ma
import matplotlib as mpl

# mpl.use('WebAgg')

fig, ax = plt.subplots(1, 1, figsize=(14,8))
plt.subplots_adjust(left=0.05, bottom=0.33, right=0.96, top=0.96)
ax.set_ylim(-100,100)
ax.set_title("mathematical simulation of flapping mechanism()")
ax.set_xlabel("time(sec)")
ax.set_ylabel("flapping degree")

axcolor = 'lightgoldenrodyellow'
dt = 0.01
t = np.arange(0.0, 1.0, dt)
ABi = 7 # center of big gear to the bar of the slider
ACi = 16.1 # center of big gear to center of slider
CDi = 25 # center of slider to attachment between slider and link
EGi = 22.5 # the distance between AC line and wing base
EFi = 8 # lenth between wingbase and the attanchment between link and wing
DFi = 25 # lenth of link
omega = ma.radians(360*2) #radian/sec
mechflapang , mechpitchang= func.SimulateFlapMechFlapAng(t*omega, ABi, ACi, CDi, EGi, EFi, DFi)
print("degrees per sec: ", ma.degrees(omega))
print("dt: ", dt)


linemechflapang, = plt.plot(t, mechflapang, **{ 'marker':',' }, label='mechenism fapping angle')
linemechpitchang, = plt.plot(t, mechpitchang, **{ 'marker':',' }, label='mechenism pitching angle')


ABax = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)
ABs = Slider(ABax, 'AB lenth', 0, 15, valinit=ABi, valstep=0.01)
ACax = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
ACs = Slider(ACax, 'AC lenth', 0, 20, valinit=ACi, valstep=0.01)
CDax = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
CDs = Slider(CDax, 'CD lenth', 0, 40, valinit=CDi, valstep=0.01)
EGax = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
EGs = Slider(EGax, 'EG lenth', 0, 30, valinit=EGi, valstep=0.01) 
EFax = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
EFs = Slider(EFax, 'EF lenth', 0, 20 ,valinit=EFi, valstep=0.01)
DFax = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
DFs = Slider(DFax, 'DF lenth', 0, 40 ,valinit=DFi, valstep=0.01)

def update(val): 
	AB = ABs.val
	AC = ACs.val
	CD = CDs.val
	EG = EGs.val
	EF = EFs.val
	DF = DFs.val
	mechflapang, mechpitch = func.SimulateFlapMechFlapAng(t*omega, AB, AC, CD, EG, EF, DF)
	linemechflapang.set_ydata(mechflapang)
	linemechpitchang.set_ydata(mechpitchang)
	fig.canvas.draw_idle()

ABs.on_changed(update)
ACs.on_changed(update)
CDs.on_changed(update)
EGs.on_changed(update)
EFs.on_changed(update)
DFs.on_changed(update)
'''
def reset(event):
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
'''

ax.legend()
plt.show()

