import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons

'''
x = np.linspace(1, 5, 50)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
ax1.plot(x, x, **{ 'marker':'x' }, label='linear')
ax2.plot(x, x**2, **{ 'marker':'X' }, label='two' )
ax3.plot(x, x**3, **{ 'marker':'v' }, label='tree' )
ax4.plot(x, x**4, **{ 'marker':'1' }, label='four' )
'''
fig, ax = plt.subplots(1, 1, figsize=(14,8))
plt.subplots_adjust(left=0.05, bottom=0.25, right=0.96, top=0.96)

axcolor = 'lightgoldenrodyellow'
t = np.arange(0.0, 1.0, 0.001)
ABi = 7
ACi = 16
DGi = 32
HIi = 24
IJi = 0.5
change = t**(ABi+ACi+DGi+HIi+IJi)

line, = plt.plot(t, change, **{ 'marker':',' }, label='linear')

ABax = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)
ABs = Slider(ABax, 'AB lenth', 0, 15, valinit=ABi, valstep=0.01)
ACax = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
ACs = Slider(ACax, 'AC lenth', 0, 20, valinit=ACi, valstep=0.01)
DGax = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
DGs = Slider(DGax, 'DG lenth', 0, 40, valinit=DGi, valstep=0.01)
HIax = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
HIs = Slider(HIax, 'HI lenth', 0, 30, valinit=HIi, valstep=0.01)
IJax = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
IJs = Slider(IJax, 'IJ lenth', 0, 1.5,valinit=IJi, valstep=0.01)

def update(val):
	AB = ABs.val
	AC = ACs.val
	DG = DGs.val
	HI = HIs.val
	IJ = IJs.val
	change = t**(AB+AC+DG+HI+IJ)
	line.set_ydata(change)
	fig.canvas.draw_idle()

ABs.on_changed(update)
ACs.on_changed(update)
DGs.on_changed(update)
HIs.on_changed(update)
IJs.on_changed(update)
'''
def reset(event):
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
'''

plt.show()

