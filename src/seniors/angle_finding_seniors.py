emport xlwings as xw
import numpy as np
import matplotlib.pyplot as plt


file_name = "leaf_rawdata"
file = xw.Book("C:\\Users\\user\\Desktop\\motion_analysis\\leaf_final_motion\\"+file_name+".xlsx")

sht_flapping = file.sheets["flapping_raw"]
sht_pitching = file.sheets["pitching_raw"]
sht_sweeping = file.sheets["sweeping_raw"]
#sht_wingtip_vel  = file.sheets["wingtip_vel_raw"]

sht_thorax_x_vel = file.sheets["thorax_xvel_raw"]
sht_thorax_y_vel = file.sheets["thorax_yvel_raw"]

#sht_head_x_vel = file.sheets["head_xvel_raw"]
#sht_head_y_vel = file.sheets["head_yvel_raw"]


point_number = 50
flapping_angle = []
pitching_angle = []
sweeping_angle = []
wingtip_vel = []
thorax_x_vel = []
thorax_y_vel = []
#head_x_vel = []
#head_y_vel = []

ncolumn = sht_flapping['a1'].expand("table").columns.count

for i in range(ncolumn):

    alpha = chr(ord('a')+i)
    nrows = file.sheets["flapping_raw"][alpha +'1'].expand("table").rows.count

    rng_flapping = sht_flapping[:nrows, i].value
    rng_pitching = sht_pitching[:nrows, i].value
    rng_sweeping = sht_sweeping[:nrows, i].value

    #rng_wingtip_vel  = sht_wingtip_vel[:nrows, i].value

    rng_thorax_x_vel = sht_thorax_x_vel[:nrows, i].value
    rng_thorax_y_vel = sht_thorax_y_vel[:nrows, i].value

    #rng_head_x_vel = sht_head_x_vel[:nrows, i].value
    #rng_head_y_vel = sht_head_y_vel[:nrows, i].value

    interval = (nrows-1) / point_number
    vel_interval = (nrows-2) / point_number

    flapping_angle.append([rng_flapping[0]])
    pitching_angle.append([rng_pitching[0]])
    sweeping_angle.append([rng_sweeping[0]])

    #wingtip_vel.append([rng_wingtip_vel [0]])
    thorax_x_vel.append([rng_thorax_x_vel[0]])
    thorax_y_vel.append([rng_thorax_y_vel[0]])

    #head_x_vel.append([rng_head_x_vel[0]])
    #head_y_vel.append([rng_head_y_vel[0]])



    for j in range(1,point_number+1):
        index = int(j*interval+0.5)
        vel_index = int(j*vel_interval+0.5)
        flapping_angle[-1].append(rng_flapping[index])
        pitching_angle[-1].append(rng_pitching[index])
        sweeping_angle[-1].append(rng_sweeping[index])
       # wingtip_vel [-1].append(rng_wingtip_vel [vel_index])
        thorax_x_vel[-1].append(rng_thorax_x_vel[vel_index])
        thorax_y_vel[-1].append(rng_thorax_y_vel[vel_index])

       # head_x_vel[-1].append(rng_head_x_vel[vel_index])
        #head_y_vel[-1].append(rng_head_y_vel[vel_index])



new_file_name = "leaf_final_motion"
new_file = xw.Book("C:\\Users\\user\\Desktop\\motion_analysis\\leaf_final_motion\\"+new_file_name+".xlsx")


new_file.sheets.add("flapping")
new_file.sheets.add("pitching")
new_file.sheets.add("sweeping")
#new_file.sheets.add("wingtip_vel")
new_file.sheets.add("thorax_x_vel")
new_file.sheets.add("thorax_y_vel")
#new_file.sheets.add("head_x_vel")
#new_file.sheets.add("head_y_vel")

interval = 1 / point_number

for j in range(point_number+1):

    new_file.sheets["flapping"][j, 0].value = interval * j
    new_file.sheets["pitching"][j, 0].value = interval * j
    new_file.sheets["sweeping"][j, 0].value = interval * j
    #new_file.sheets["wingtip_vel"][j, 0].value = interval * j

    new_file.sheets["thorax_x_vel"][j, 0].value = interval * j
    new_file.sheets["thorax_y_vel"][j, 0].value = interval * j

    #new_file.sheets["head_x_vel"][j, 0].value = interval * j
    #new_file.sheets["head_y_vel"][j, 0].value = interval * j


    for i in range(len(flapping_angle)):
        new_file.sheets["flapping"][j, i + 1].value = flapping_angle[i][j]
        new_file.sheets["pitching"][j, i + 1].value = pitching_angle[i][j]
        new_file.sheets["sweeping"][j, i + 1].value = sweeping_angle[i][j]
        #new_file.sheets["wingtip_vel"][j, i + 1].value = wingtip_vel [i][j]
        new_file.sheets["thorax_x_vel"][j, i + 1].value = thorax_x_vel[i][j]
        new_file.sheets["thorax_y_vel"][j, i + 1].value = thorax_y_vel[i][j]

       # new_file.sheets["head_x_vel"][j, i + 1].value = head_x_vel[i][j]
       # new_file.sheets["head_y_vel"][j, i + 1].value = head_y_vel[i][j]
