import xlwings as xw
# import numpy as np
# import matplotlib.pyplot as plt
import pprint
import json as js
import tkinter as tk
import jack_functions as func

# read data from excel file
file_name = func.tk_GetFileName()
database = xw.Book(file_name)
nrows = database.sheets[2]["a1"].expand("table").rows.count 
print(nrows-2)
data = database.sheets["data"]
side_wb = (data[f"a3:b"+str(nrows)].value)  # wingbase
side_wt = (data[f"c3:d"+str(nrows)].value)  # wingtip
side_te = (data[f"e3:f"+str(nrows)].value)  # hindwing trailing edge
side_ta = (data[f"g3:h"+str(nrows)].value)  # tail

top_wb = (data[f"i3:j"+str(nrows)].value)  # wingbase
top_wt = (data[f"k3:l"+str(nrows)].value)  # wingtip
top_te = (data[f"m3:n"+str(nrows)].value)  # hindwing trailing edge
top_ta = (data[f"o3:p"+str(nrows)].value)  # tail
print("finnish colecting data")
data = get_Jsonrawdb()
print(type(data))
pp = pprint.PrettyPrinter(indent=2)
side_dic = {
	"wing_base":side_wb,
	"wing_tip" :side_wt,
	"trailing_edge" :side_te,
	"tail" :side_ta
}
top_dic = {
	"wing_base":top_wb,
	"wing_tip" :top_wt,
	"trailing_edge" :top_te,
	"tail" :top_ta
}
data[file_name] = {
	"side":side_dic, 
	"top":top_dic
}

write_Jsondb(data)
print(type(data))

