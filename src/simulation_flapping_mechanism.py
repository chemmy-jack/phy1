import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
import jack_functions as func
import math as ma

fig, ax = plt.subplots(1, 1, figsize=(14,8))
plt.subplots_adjust(left=0.05, bottom=0.33, right=0.96, top=0.96)
ax.set_ylim(-90,90)
ax.set_title("mathematical simulation of flapping mechanism()")
ax.set_xlabel("time(sec)")
ax.set_ylabel("flapping degree")

axcolor = 'lightgoldenrodyellow'
dt = 0.01
t = np.arange(0.0, 1.0, dt)
ABi = 7
ACi = 16
DGi = 32
HIi = 24
IJi = 15
GJi = 30
omega = ma.radians(360*2) #radian/sec
change = func.SimulateFlapMechFlapAng(t*omega, ABi, ACi, DGi, HIi, IJi, GJi)
print("degrees per sec: ", ma.degrees(omega))
print("dt: ", dt)


line, = plt.plot(t, change, **{ 'marker':',' }, label='fapping')

ABax = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)
ABs = Slider(ABax, 'AB lenth', 0, 15, valinit=ABi, valstep=0.01)
ACax = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
ACs = Slider(ACax, 'AC lenth', 0, 20, valinit=ACi, valstep=0.01)
DGax = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
DGs = Slider(DGax, 'DG lenth', 0, 40, valinit=DGi, valstep=0.01)
HIax = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
HIs = Slider(HIax, 'HI lenth', 0, 30, valinit=HIi, valstep=0.01)
IJax = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
IJs = Slider(IJax, 'IJ lenth', 0, 20 ,valinit=IJi, valstep=0.01)
GJax = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
GJs = Slider(GJax, 'GJ lenth', 0, 40 ,valinit=GJi, valstep=0.01)

def update(val): 
	AB = ABs.val
	AC = ACs.val
	DG = DGs.val
	HI = HIs.val
	IJ = IJs.val
	GJ = GJs.val
	change = func.SimulateFlapMechFlapAng(t*omega, AB, AC, DG, HI, IJ, GJ)
	line.set_ydata(change)
	fig.canvas.draw_idle()

ABs.on_changed(update)
ACs.on_changed(update)
DGs.on_changed(update)
HIs.on_changed(update)
IJs.on_changed(update)
GJs.on_changed(update)
'''
def reset(event):
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
'''

ax.legend()
plt.show()

