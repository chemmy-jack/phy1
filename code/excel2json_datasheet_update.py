import xlwings as xw
# import numpy as np
# import matplotlib.pyplot as plt
# import pprint
import json as js
# read data from excel file
# file_name = input("witch excel file(files will be find in /Volumes/JACK4/filename.xlsx, and use the 'data' sheet which contains 16rows): ")
import sys

def update(file_name) :
	database = xw.Book("/Volumes/JACK4/"+file_name+".xlsx")
	nrows = database.sheets[2]["a1"].expand("table").rows.count 
	print(nrows-2)
	exceldata = database.sheets["data"]
	side_wb = (exceldata[f"a3:b"+str(nrows)].value)  # wingbase
	side_wt = (exceldata[f"c3:d"+str(nrows)].value)  # wingtip
	side_te = (exceldata[f"e3:f"+str(nrows)].value)  # hindwing trailing edge
	side_ta = (exceldata[f"g3:h"+str(nrows)].value)  # tail
	top_wb = (exceldata[f"i3:j"+str(nrows)].value)  # wingbase
	top_wt = (exceldata[f"k3:l"+str(nrows)].value)  # wingtip
	top_te = (exceldata[f"m3:n"+str(nrows)].value)  # hindwing trailing edge
	top_ta = (exceldata[f"o3:p"+str(nrows)].value)  # tail 
	print("finnish colecting data of excel data sheet")
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
	print("this is the new json: ")
	# pp.pprint(data)
	with open ("../db/rawtopside.json", "w") as database:
		# database.write(js.dumps(data, indent=4))
		database.write(js.dumps(data))

with open ("../db/rawtopside.json", "r") as database:
	data = js.loads(database.read())
print(type(data))
# pp = pprint.PrettyPrinter(indent=2)
i = 0
print(i,end = " ")
print("all")
for x in data :
	i += 1
	print(i,end = " ")
	print(x,end = " ")
	print(len(data[x]))

n =input('type the number required to update: ' )
try :
	n = int(n)
except ValueError:
	print("not integer")
	sys.exit()

if n == 0 :
	for x in data :
		print(i,end = " ")
		print(x,end = " ")
		print(len(data[x]))
		update(x)
else :
	N = len(list(data.keys()))
	if n<0 or n>N : 
		print("error: no such file")
		sys.exit()
	for x in data :
		N -= 1
		if N == 0 :
			print(i,end = " ")
			print(x,end = " ")
			print(len(data[x]))
			update(x)
