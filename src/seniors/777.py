# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:21:55 2019

@author: User
"""

import xlwings as xw
import numpy as np
import matplotlib.pyplot as plt


file_name = "0814_3_13_1_new"
file = xw.Book("C:\\Users\\user\\Desktop\\motion_analysis\\leaf_final_motion\\"+file_name+".xlsx")

nrows = file.sheets[0]["a1"].expand("table").rows.count

side_head = -1*np.array(file.sheets["side_head"][f"a1:b{nrows}"].value)
side_thorax = -1*np.array(file.sheets["side_thorax"][f"a1:b{nrows}"].value)
side_wt = -1*np.array(file.sheets["side_wingtip"][f"a1:b{nrows}"].value)  # wingtip
side_wb = -1*np.array(file.sheets["side_wingbase"][f"a1:b{nrows}"].value)  # wingbase
side_te = -1*np.array(file.sheets["side_trailingedge"][f"a1:b{nrows}"].value)  # hindwing trailing edge
#side_tail = -1*np.array(file.sheets["side_tail"][f"a1:b{nrows}"].value)
#side_hindle = -1*np.array(file.sheets["side_hindle"][f"a1:b{nrows}"].value)



top_head = np.array(file.sheets["top_head"][f"a1:b{nrows}"].value)
top_thorax = np.array(file.sheets["top_thorax"][f"a1:b{nrows}"].value)
top_wt = np.array(file.sheets["top_wingtip"][f"a1:b{nrows}"].value)  # wingtip
top_wb = np.array(file.sheets["top_wingbase"][f"a1:b{nrows}"].value)  # wingbase
top_te = np.array(file.sheets["top_trailingedge"][f"a1:b{nrows}"].value)  # hindwing trailing edge
#top_tail = np.array(file.sheets["top_tail"][f"a1:b{nrows}"].value)
#top_hindle = np.array(file.sheets["top_hindle"][f"a1:b{nrows}"].value)

thorax_xvel_file = open(file_name +"_thorax_Xvel.txt",'w')
thorax_yvel_file = open(file_name +"_thorax_Yvel.txt",'w')

#head_xvel_file = open(file_name +"_head_Xvel.txt",'w')
#head_yvel_file = open(file_name +"_head_Yvel.txt",'w')





#wingtip_vel_file = open(file_name +"_wingtip_vel.txt",'w')

for i in range(1,len(side_head)):


    thorax_xvel_file.writelines(str((side_thorax[i][0]-side_thorax[i-1][0])*10))
    thorax_xvel_file.writelines("\n")

    #head_xvel_file.writelines(str((side_head[i][0]-side_head[i-1][0])*10))
   # head_xvel_file.writelines("\n")

    thorax_yvel_file.writelines(str((side_thorax[i][1] - side_thorax[i -1][1])*10))
    thorax_yvel_file.writelines("\n")

    #head_yvel_file.writelines(str((side_head[i][1] - side_head[i - 1][1]) * 10))
    #head_yvel_file.writelines("\n")

    #tip_vel = np.sqrt((side_wt[i][0]-side_wt[i-1][0])**2 + (side_wt[i][1]-side_wt[i-1][1])**2 + (top_wt[i][1]-top_wt[i-1][1])**2)*10
    #wingtip_vel_file.writelines(str(tip_vel))
    #wingtip_vel_file.writelines("\n")

#head_xvel_file.close()
#head_yvel_file.close()
thorax_xvel_file.close()
thorax_yvel_file.close()

body_vector =[]
le_vector =[]
hind_te_vector =[]

#hind_le_vector=[]


# offset

for i in range(nrows):
    top_head[i][0] *= -1
    top_thorax[i][0] *= -1
    top_wt[i][0] *= -1
    top_wb[i][0] *= -1
    top_te[i][0] *= -1

    #top_hindle[i][0] *= -1

    #top_tail[i][0] *= -1

temp_head = []
temp_le = []
temp_te = []




for i in range(nrows):
    for j in range(2):
        side_head[i][j] -= side_thorax[i][j]
        side_wt[i][j] -= side_wb[i][j]
        #side_wb[i][j] -=side_thorax[i][j]
        side_te[i][j] -= side_wb[i][j]

        #side_hindle[i][j] -= side_wb[i][j]

        #side_tail[i][j] -=side_thorax[i][j]
        #side_thorax[i][j] -= side_thorax[i][j]

        top_head[i][j] -= top_thorax[i][j]
        top_wt[i][j] -= top_wb[i][j]
       # top_wb[i][j] -=top_thorax[i][j]
        top_te[i][j] -= top_wb[i][j]
       # top_hindle[i][j] -= top_wb[i][j]



       # top_tail[i][j] -=top_thorax[i][j]
        #top_thorax[i][j] -= top_thorax[i][j]

    #side_head[i][1] *= abs(top_head[i][0]/ side_head[i][0])
    #top_thorax[i][1] *= side_thorax[i][0] / top_thorax[i][0]
    #top_wt[i][1] *= side_wt[i][0] / top_wt[i][0]
   # side_wt[i][1] *=  abs(top_wt[i][0]/side_wt[i][0])
    #side_te[i][1] *= abs(top_te[i][0]/side_te[i][0])
    #top_wb[i][1] *= side_wb[i][0] / top_wb[i][0]
    #top_te[i][1] *= side_te[i][0] / top_te[i][0]
    #top_tail[i][1] *= side_tail[i][0] / top_tail[i][0]

    #temp_head.append(top_head[i][0] / side_head[i][0])
    #temp_le.append( top_wt[i][0]/side_wt[i][0])
    #temp_te.append( top_te[i][0] / side_te[i][0])


    body_vector.append([(side_head[i][0] + top_head[i][0])/2 , side_head[i][1], top_head[i][1]])
    le_vector.append([(side_wt[i][0]+top_wt[i][0])/2 , side_wt[i][1], top_wt[i][1]])
    hind_te_vector.append([(side_te[i][0]+top_te[i][0])/2 , side_te[i][1], top_te[i][1]])
    #hind_le_vector.append([(side_hindle[i][0]+top_hindle[i][0])/2 , side_hindle[i][1], top_hindle[i][1]])



body_vector = np.array(body_vector)
le_vector = np.array(le_vector)
hind_te_vector = np.array(hind_te_vector)

#hind_le_vector = np.array(hind_le_vector )
"""
head = np.array(head)
thorax = np.array(thorax)
wb = np.array(wb)
wt = np.array(wt)
te = np.array(te)
tail = np.array(tail)

body_vector = head - thorax
le_vector = wt - wb
hind_te_vector = te - wb
"""
sweeping_angle = []
pitching_angle = []
flapping_angle = []

hind_sweeping_angle= []


wingplane_vector = []
for i in range(nrows):

    wingplane_normal_vector = np.cross(le_vector[i], hind_te_vector[i])
    temp = wingplane_normal_vector[:]

    temp_len = np.sqrt(temp[0]**2+temp[1]**2+temp[2]**2)
    temp[0] /= temp_len
    temp[1] /= temp_len
    temp[2] /= temp_len

    wingplane_vector.append([str(temp[0])+" "+str(temp[1])+" "+str(temp[2])])

    sw_base_vector = np.cross(wingplane_normal_vector, body_vector[i])
    len_sw_base = np.sqrt(np.dot(sw_base_vector, sw_base_vector))
    len_le = np.sqrt(np.dot(le_vector[i], le_vector[i]))

    #len_hind_le = np.sqrt(np.dot(hind_le_vector[i], hind_le_vector[i]))

    sw_temp = np.arccos(np.dot(sw_base_vector, le_vector[i]) / (len_sw_base * len_le)) * 180 / np.pi

    #sw_temp1 = np.arccos(np.dot(sw_base_vector, hind_le_vector[i]) / (len_sw_base * len_hind_le)) * 180 / np.pi


    sweeping_angle.append(sw_temp)
    #hind_sweeping_angle.append(sw_temp1)
    #len_body_vector = np.sqrt(np.dot(body_vector[i],body_vector[i]))
    #pitching_base = np.array([body_vector[i][0],0,body_vector[i][2]])
    #len_pitching_base = np.sqrt(np.dot(pitching_base,pitching_base))
    #pitching_angle.append(np.arccos(np.dot(body_vector[i],pitching_base)/(len_pitching_base*len_body_vector)) * 180 / np.pi)

    pitching_angle.append(np.arctan(body_vector[i][1]/body_vector[i][0])* 180 / np.pi)


    body_left_temp_x = -body_vector[i][2] * np.sqrt(body_vector[i][0] ** 2 + body_vector[i][2] ** 2)
    body_left_temp_z = body_vector[i][0] * np.sqrt(body_vector[i][0] ** 2 + body_vector[i][2] ** 2)
    # body_right_vector = np.array([body_right_temp_x,wb[i][1],body_right_temp_z])
    body_left_vector = np.array([body_left_temp_x, 0, body_left_temp_z])

    len_body_left = np.sqrt(np.dot(body_left_vector, body_left_vector))

    flap_temp = np.dot(sw_base_vector, body_left_vector) / (len_sw_base * len_body_left)
    #flap_temp = np.dot(sw_base_vector, [0, 0, -1]) / (len_sw_base)

    if sw_base_vector[1] > 0:
        flap_temp = np.arccos(flap_temp) * 180 / np.pi
    else:
        flap_temp = -np.arccos(flap_temp) * 180 / np.pi

    flapping_angle.append(-flap_temp)



flapping_file = open(file_name + "_flapping.txt", 'w')
pitching_file = open(file_name + "_pitching.txt", 'w')
sweeping_file =  open(file_name + "_sweeping.txt", 'w')


"""
#wingplane_file = open(file_name + "_wingplane.txt", 'w')
for i in range(len(wingplane_vector)):
    wingplane_file.writelines(wingplane_vector[i])
    wingplane_file.writelines("\n")
wingplane_file.close()

"""


for i in range(len(flapping_angle)):
    flapping_file.writelines(str(flapping_angle[i]))
    flapping_file.writelines("\n")
    pitching_file.writelines(str(pitching_angle[i]))
    pitching_file.writelines("\n")
    sweeping_file.writelines(str(sweeping_angle[i]))
    sweeping_file.writelines("\n")


    
flapping_file.close()
pitching_file.close()
sweeping_file.close()



temp = np.arange(0, nrows)
plt.plot(temp, pitching_angle)
#plt.plot(temp, flapping_angle,label = "flapping")
#plt.plot(temp,sweeping_angle,label = "sweeping")

plt.grid()
plt.show()
