import xlwings as xw
import json as js
import tkinter as tk
from tkinter import filedialog
import git
import sys
import os
from math import cos, sin, asin, acos, tan, atan, radians, degrees
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ != "__main__" :
	importedby_path = sys._getframe(1).f_globals.get('__name__')
	print('jack function is being imported by',importedby_path)

def get_git_root(path):
	git_repo = git.Repo(path, search_parent_directories=True)
	git_root = git_repo.git.rev_parse("--show-toplevel")
	print(git_root)
	return(git_root)

def GetDatabasePath() :
	mypath = os.path.dirname(os.path.realpath(__file__))
	toreturn = str(get_git_root(mypath))+ "/db/rawtopside.json" # this is asuming this scipt is under git repo and databasejson is under gitroot/db/rawtopside.json
	return toreturn

database = GetDatabasePath()

def cal_origin_coordinate(spec_data) :
	# check same lenth of rows
	key1 = list(spec_data.keys())[0]
	key1_1 = list(spec_data[key1].keys())[0]
	nrows = len(spec_data[key1][key1_1])
	for x in spec_data :
		for y in spec_data[x] :
			print("{:4}".format(x),end=" ")
			print("{:15}".format(y),end=" ")
			print(len(spec_data[x][y]))
			# if len(y) != nrows :return print("error: row lenth not the same")
	o_wb = []
	o_wt = []
	o_te = []
	o_ta = []
	for i in range(nrows):
		o_wb.append([-(spec_data["side"]["wing_base"][i][0] + spec_data["top"]["wing_base"][i][0]) / 2, spec_data["side"]["wing_base"][i][1], -spec_data["top"]["wing_base"][i][1]])
		o_wt.append([-(spec_data["side"]["wing_tip"][i][0] + spec_data["top"]["wing_tip"][i][0]) / 2, spec_data["side"]["wing_tip"][i][1], -spec_data["top"]["wing_tip"][i][1]])
		o_te.append([-(spec_data["side"]["trailing_edge"][i][0] + spec_data["top"]["trailing_edge"][i][0]) / 2, spec_data["side"]["trailing_edge"][i][1], -spec_data["top"]["trailing_edge"][i][1]])
		o_ta.append([-(spec_data["side"]["tail"][i][0] + spec_data["top"]["tail"][i][0]) / 2, spec_data["side"]["tail"][i][1], -spec_data["top"]["tail"][i][1]])
	return { "wb":o_wb, "wt":o_wt, "te":o_te, "ta":o_ta}

def tk_GetFileName() :
	root = tk.Tk()
	root.withdraw()
	FileName = filedialog.askopenfilename()
	return FileName

def get_Jsonrawdb() :
	with open (database, "r") as databasetmp:
		data = js.loads(databasetmp.read())
	return data

def write_Jsondb(data) :
	with open ("../db/rawtopside.json", "w") as databasetmp:
		databasetmp.write(js.dumps(data, indent=4))

def PrintKeysWithNum(data) :
	n = 1
	for x in data :
		try :
			key1_1 = list(data[x].keys())[0]
			key1_1_1 = list(data[x][key1_1].keys())[0]
			nrows = len(data[x][key1_1][key1_1_1])
		except :
			nrows = 0
		print("{:2} {:3} ".format(n,nrows),x)
		n += 1
	return n-1

def GetSpecKeyByNum(data) :
	# print possibles
	n = PrintKeysWithNum(data)
	# choose specfic
	N = input("type number to choose: ")
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
			spec_data_name = x
			return spec_data_name
	
def GetMtrackRawDataSheet(sheet) : # assume a:Nr, b:TID, c:PID, d:x, e:c
	nrows = sheet["a1"].expand("table").rows.count 
	Nr = sheet[f"a2:a"+str(nrows)].value
	TID = sheet[f"b2:b"+str(nrows)].value
	PID = sheet[f"c2:c"+str(nrows)].value
	x = sheet[f"d2:d"+str(nrows)].value
	y = sheet[f"e2:e"+str(nrows)].value
	data = {
		"nr":Nr,
		"tid":TID,
		"pid":PID,
		"x":x,
		"y":y }
	return data

def FindArrayInclude(array) :
	include = {}
	for i in array :
		if i in include :
			include[int(i)] += 1
		else : include[int(i)] = 1
	return include

def GetExcelRawTopSide(exel_file) :
	sheettop = exel_file.sheets["raw_data_top"]
	sheetside = exel_file.sheets["raw_data_side"]
	datatop = GetMtrackRawDataSheet(sheettop)
	dataside = GetMtrackRawDataSheet(sheetside)
	TIDtop = FindArrayInclude(datatop["tid"])
	TIDside = FindArrayInclude(dataside["tid"])
	print("\nfind top TID: ", end = "\n")
	for i in TIDtop :	
		print(i , ": ", TIDtop[i], end = "\n")
	print("\nfind side TID: ", end = "\n")
	for i in TIDside :	
		print(i, ": ", TIDside[i], end = "\n")
	
	# get top 
	while True :
		try : 
			temp = int(input("top wb: "))
			top_wb = TIDtop.pop(temp)
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top wt: "))
			top_wt =TIDtop.pop(temp)
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top te: "))
			top_te =TIDtop.pop(temp)
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top ta: "))
			top_ta =TIDtop.pop(temp)
			break
		except : print("error: try again")

	# get side 
	while True :
		try : 
			temp = int(input("side wb: "))
			side_wb = TIDside.pop(temp)
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side wt: "))
			side_wt =TIDside.pop(temp)
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side te: "))
			side_te =TIDside.pop(temp)
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side ta: "))
			side_ta =TIDside.pop(temp)
			break
		except : print("error: try again")

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
	data = {
		"side":side_dic, 
		"top":top_dic
	}
	return data


def SimulateFlapMechFlapAng(a,b,c,d,h,i,g) : #theta,AB,AC,DG,IH,IJ,GJ
#	BC2 = b**2 + c**2 - 2*b*c*math.cos(math.radians(a))
	C = [c,0]
	flapang = []
	pitchang = []
	for x in a :
		B = [b*cos(x),b*sin(x)]
		BC = np.subtract(C, B)
		try :
			if x == 0 : pitchang.append(None)
			else : pitchang.append(degrees(atan(BC[1]/ BC[0])))
#			pitchang.append(atan(BC[0]/ BC[1]))
		except :
			pitchang.append(None)
		CG = BC*d/np.linalg.norm(BC)
		G = np.add(C, CG)
		I = [c+d, h]
		GI = np.linalg.norm(np.subtract(I, G))
		try : 
			flapang.append(degrees(acos((i**2 + GI**2 - g**2)/(2*i*g)))-90)
#			flapang.append(((i**2 + GI**2 - g**2)/(2*i*g)))
		except : flapang.append(None)
	return flapang, pitchang

def GetExcelDataSheet(database) : # assumes each row have same lenth
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
	data = {
		"side":side_dic, 
		"top":top_dic
	}
	return data

