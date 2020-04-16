import xlwings as xw
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
from scipy.ndimage.interpolation import rotate

# read data from excel file
file_name = "0831_4_1"
database = xw.Book("/Volumes/JACK4/"+file_name+".xlsx")
nrows = database.sheets[2]["a1"].expand("table").rows.count 
print(nrows-2)
data = database.sheets["data"]
side_wb = np.array(data[f"a3:b"+str(nrows)].value)  # wingbase
side_wt = np.array(data[f"c3:d"+str(nrows)].value)  # wingtip
side_te = np.array(data[f"e3:f"+str(nrows)].value)  # hindwing trailing edge
side_ta = np.array(data[f"g3:h"+str(nrows)].value)  # tail

top_wb = np.array(data[f"i3:j"+str(nrows)].value)  # wingbase
top_wt = np.array(data[f"k3:l"+str(nrows)].value)  # wingtip
top_te = np.array(data[f"m3:n"+str(nrows)].value)  # hindwing trailing edge
top_ta = np.array(data[f"o3:p"+str(nrows)].value)  # tail
print("finnish colecting data")
#multiply top[0] with 1280/800 and top[1] with 800/600(if resolution weren't the same)(top:800*600, side:1280*800)
#print("finnish colecting data and multiply top with 2180/800")

# calculate origin coordinate
nrows -= 2
o_wb = []
o_wt = []
o_te = []
o_ta = []
for i in range(nrows):
    o_wb.append([-(side_wb[i][0] + top_wb[i][0]) / 2, side_wb[i][1], -top_wb[i][1]])
    o_wt.append([-(side_wt[i][0] + top_wt[i][0]) / 2, side_wt[i][1], -top_wt[i][1]])
    o_te.append([-(side_te[i][0] + top_te[i][0]) / 2, side_te[i][1], -top_te[i][1]])
    o_ta.append([-(side_te[i][0] + top_te[i][0]) / 2, side_ta[i][1], -top_ta[i][1]])
print("finnish calculate origin coordinate")


# analysing track from outer cordinate
wb_xytrack = [[0,0]] #翼根軌跡(print)
for i in range(nrows): 
    temp = np.subtract(o_wb[i], o_wb[0])
    wb_xytrack.append([LA.norm([temp[0],temp[2]]),-temp[1]])
print("analysing track from outer cordinate")

# calculate directon方向角 & mean direction
direct = []
for i in range(nrows):
    direct.append( np.arctan( o_wb[i][0]-o_ta[i][0] / o_wb[i][2]-o_ta[i][2] ) )
mean_direct = np.mean(direct) # 平均方向角 計算偏移角用 投影xy平面用
print(mean_direct)
print("finnish calculate directon方向角 & mean direction")

# calculate inner coordinate
wt = []
te = []
ta = []
for i in range(nrows): 
    wt.append(np.subtract(o_wt[i], o_wb[i]))
    te.append(np.subtract(o_te[i], o_wb[i]))
    ta.append(np.subtract(o_ta[i], o_wb[i]))
print("finnish calculate inner coordinate")

# rotate inner coordinate
## calculate shift_angle偏移角度
shift_angle = [] # 偏移角(print)
for i in range(nrows): 
    shift_angle.append(mean_direct-direct[i] )
    #print(shift_angle[i])
print("...calculate shift_angle偏移角度")
'''
## rotate inner coordinate
for i in range(nrows):
    print("rotate"+str(i))
    print(ta[i]) 
    theta = direct[i]
    print(theta)
    c, s = np.cos(theta), np.sin(theta)
    R = [[-s, c], [c, s] ]
    temp = np.dot([ta[i][0],ta[i][2]], R)
    ta[i][0], ta[i][2] = temp[0], temp[1]
    print(ta[i])
print("finnish rotate inner coordinate")
'''

# calculate abdomen angle
abdomen_angle = [] #腹部角(print)
for i in range(nrows):
    abdomen_angle.append(np.degrees(np.arctan(ta[i][1]/np.sqrt(ta[i][0]**2 + ta[i][2]**2))))
print("finnish calculating abdomen angle")

# calculate flapping angle (angle between LEvector unit wingbase z axis vector)
flapping_angle = [] #拍撲角(print)
for i in range(nrows):
    temp = [ta[i][2],0,ta[i][0]]
    flapping_angle.append(np.degrees(np.arccos(np.dot(temp/LA.norm(temp),wt[i]/LA.norm(wt[i])))))
    if wt[i][1]>0 : flapping_angle[i] *= -1
    print(wt[i][1])
print("finnish caculate flapping angle")

# calculate wing rotate angle
wingrotate_angle = [] #翅膀旋轉(print) 
## calculate delta ta vector
delta_ta = []
for i in range(3): ta.append(ta[-1])
for i in range(nrows):
    delta_ta.append(np.subtract(ta[i+2], ta[i-2])/2)
print("...finnish calculate delta ta vector")
## calcutate normal vector of wing
normal_wing = []
for i in range(nrows):
    normal_wing.append(np.cross(wt[i],te[i]))
print("...finnish calcutate normal vector of wing")
## calculate wing rotate angle
for i in range(nrows):
    wingrotate_angle.append(90-np.degrees(np.arccos(np.dot(normal_wing[i]/LA.norm(normal_wing[i]),delta_ta[i]/LA.norm(delta_ta[i])))))
print("finnish caculate wing rotate angle")

# calculate pitching angle
pitching_angle = [] #仰角 flapping axis與horizon之angle (print)
for i in range(nrows):
    temp = [ta[i][2],0,ta[i][0]]
    #print(delta_ta[i])
    unit_delta_ta = delta_ta[i]/LA.norm(delta_ta[i])
    #print(unit_delta_ta)
    unit_temp = temp/LA.norm(temp)
    flapping_axis = np.cross(unit_delta_ta, unit_temp)
    #print(flapping_axis)
    temp =  flapping_axis[1]/np.sqrt(flapping_axis[0]**2 + flapping_axis[2]**2) 
    #print(temp)
    pitching_angle.append(np.degrees(np.arctan(temp)))
print("finnish calculate pitching angle")


#create analys sheet
try :
    print(database.sheets["analys"])
except :
    database.sheets.add(name="analys",after=-1)
    print(database.sheets["analys"])
analys = database.sheets["analys"]

printanglelist = [
    ["abdomen_angle",abdomen_angle,"b"],
    ["flapping_angle",flapping_angle,"c"],
    ["wingrotate_angle",wingrotate_angle,"d"],
    ["pitching_angle",pitching_angle,"e"]
]

#create number (if no number)
if analys["a"+str(1+1)].value != str(1) :
    for i in range(1,nrows+1):
        analys["a"+str(i+1)].value = str(i)
    print("side bar number create finnish")

for n in printanglelist :
    print(n)
    analys[n[2]+"1"].value = n[0]
    for i in range(1,nrows+1):
        analys[n[2]+str(i+1)].value = str(n[1][i-1])
    print(n[0]+"finnished")


analys["f"+str(1)].value = "wb_xytrack"
for i in range(1,nrows+1):
    analys["f"+str(i+1)].value = str(wb_xytrack[i-1][0])
    analys["g"+str(i+1)].value = str(wb_xytrack[i-1][1])
print("track finnished")

'''
#flapping_angle 
analys["b"+str(1)].value = "flapping angle"
for i in range(1,nrows+1):
    analys["b"+str(i+1)].value = str(flapping_angle[i-1])
print("flapping angle sheet finnished")
# abdomen_angle 
analys["c"+str(1)].value = "abdomen angle"
for i in range(1,nrows+1):
    analys["c"+str(i+1)].value = str(abdomen_angle[i-1])
print("abdomen angle sheet finnished")
# sweeping_angle 
analys["d"+str(1)].value = "sweeping angle"
for i in range(1,nrows+1):
    analys["d"+str(i+1)].value = str(sweeping_angle[i-1])
print("sweeping angle sheet finnished")
'''

# for i in range(nrows):
#    print(str(abdomen_angle[i])+"|"+str(flapping_angle[i])+"|"+str(pitching_angle[i])+"|"+str(wingrotate_angle[i]))

temp = np.arange(0, nrows)
plt.plot(temp,abdomen_angle,label = "abdomen")
plt.plot(temp,flapping_angle,label = "flapping")
plt.plot(temp,pitching_angle,label = "pitching")
plt.plot(temp,wingrotate_angle,label = "wingrotate_angle")
plt.legend()
plt.show()
