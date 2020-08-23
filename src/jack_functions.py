from json import dumps, loads
from tkinter import filedialog
import tkinter as tk
from git import Repo
import sys
from math import cos, sin, asin, acos, tan, atan, radians, degrees, sqrt
from numpy import dot, cross, subtract, linalg, add, mean 
import pprint
pp = pprint.PrettyPrinter()

# for analyse
import matplotlib.pyplot as plt
from numpy import linalg as LA
from scipy.ndimage.interpolation import rotate

# for csv
from os import listdir, path
import csv

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
	git_repo = Repo(path, search_parent_directories=True)
	git_root = git_repo.git.rev_parse("--show-toplevel")
	print(git_root)
	return(git_root)

def GetDatabasePath(iswhat = "don't know") :
	mypath = path.dirname(path.realpath(__file__))
	if iswhat == "butterfly" : dbname = "/db/rawtopside.json" 
	elif iswhat == "ornithopter" : dbname = "/db/rawtopside_orn.json" 
	elif iswhat == "don't know" : 
		print("require butterfly or ornithopter")
		exit()
	else : exit()
	toreturn = str(get_git_root(mypath))+ dbname # this is asuming this scipt is under git repo and databasejson is under gitroot/db/rawtopside.json
	return toreturn

def get_Jsonrawdb(iswhat = "don't know") :
	if iswhat == "butterfly" : dbname = "/db/rawtopside.json" 
	elif iswhat == "ornithopter" : dbname = "/db/rawtopside_orn.json" 
	elif iswhat == "don't know" : 
		iswhat = ChooseOneWithNum(["butterfly", "ornithopter"])
	else : exit()
	with open (GetDatabasePath(iswhat), "r") as databasetmp:
		data = loads(databasetmp.read())
	return data

def write_Jsondb(data, iswhat = "don't know") :
	if iswhat == "butterfly" : dbname = "/db/rawtopside.json" 
	elif iswhat == "ornithopter" : dbname = "/db/rawtopside_orn.json" 
	elif iswhat == "don't know" : 
		print("require butterfly or ornithopter")
		exit()
	else : exit()
	with open (dbname, "w") as databasetmp:
		buff = dumps(data, indent=4, sort_keys = True)
		databasetmp.write(buff)
	print(bcolors.FAIL, "confirm : json raw database updated", bcolors.ENDC)



def tk_GetFilePath() :
	root = tk.gTk()
	root.withdraw()
	FileName = filedialog.askopenfilename()
	return FileName

def tk_GetFolderPath() :
	root = tk.gTk()
	root.withdraw()
	mypath = filedialog.askdirectory()
	return maypath

def cal_origin_coordinate(spec_data, iswhat = "don't know") :
		if iswhat == "butterfly" or iswhat == "ornithoter" : orn_but = iswhat
		else : orn_but = ChooseOneWithNum(["ornithopter", "butterfly"])
		if orn_but == "ornithopter" :
			orn = True
			nrows = 0
		else :
			orn = False
			nrows = 10000000
		for x in spec_data :
			for y in spec_data[x] :
				print("{:4}".format(x),end=" ")
				print("{:15}".format(y),end=" ")
				row = len(spec_data[x][y]) 
				print(row)
				if orn :
					if nrows < row :
						nrows = row
				elif nrows > row :
					nrows = row
		print(nrows)
			

				# if len(y) != nrows :return print("error: row lenth not the same")
		o_wb = []
		o_wt = []
		o_te = []
		o_ta = []
		for i in range(nrows):
			o_wt.append([-(spec_data["side"]["wing_tip"][i][0] + spec_data["top"]["wing_tip"][i][0]) / 2, -spec_data["side"]["wing_tip"][i][1], -spec_data["top"]["wing_tip"][i][1]])
			o_te.append([-(spec_data["side"]["trailing_edge"][i][0] + spec_data["top"]["trailing_edge"][i][0]) / 2, -spec_data["side"]["trailing_edge"][i][1], -spec_data["top"]["trailing_edge"][i][1]])
			if orn :
				i = 0
			o_ta.append([-(spec_data["side"]["tail"][i][0] + spec_data["top"]["tail"][i][0]) / 2, -spec_data["side"]["tail"][i][1], -spec_data["top"]["tail"][i][1]])
			o_wb.append([-(spec_data["side"]["wing_base"][i][0] + spec_data["top"]["wing_base"][i][0]) / 2, -spec_data["side"]["wing_base"][i][1], -spec_data["top"]["wing_base"][i][1]])
		return { "wb":o_wb, "wt":o_wt, "te":o_te, "ta":o_ta}

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
	
def ChooseOneWithNum(a) : # give me an array of options
	dic = {}
	n = 0
	for x in a :
		n += 1
		dic[n] = x
		print(bcolors.FAIL, n, bcolors.ENDC, x)
	print(bcolors.FAIL, n+1,bcolors.ENDC , "escape")
	while True :
		try :
			m = input("choose one : ")
			m = int(m)
			if m > 0 and m <= n :
				print("confirm : you chose ", bcolors.FAIL, str(dic[m]), bcolors.ENDC)
				print("\n")
				return dic[m]
			if m == n+1 :
				return None
		except : continue

def GetMtrackRawDataSheet(sheet) : # assume a:Nr, b:TID, c:PID, d:x, e:c
	nrows = sheet["a1"].expand("table").rows.count 
	Nr = sheet[f"a2:a"+str(nrows)].value
	TID = sheet[f"b2:b"+str(nrows)].value
	PID = sheet[f"c2:c"+str(nrows)].value
	x = sheet[f"d2:d"+str(nrows)].value
	y = sheet[f"e2:e"+str(nrows)].value
	x_y = []
	nrows -= 1
	for i in range(nrows) :
		x_y.append([x[i],y[i]])
	data = {
		"nr":Nr,
		"tid":TID,
		"pid":PID,
		"x_y":x_y }
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

	# make TID to [x, y]
	## top
	totalnum = len(datatop["nr"])
	tid2co_top = {}
	for i in range(totalnum) :
		tid = datatop["tid"][i] 
		if tid not in tid2co_top :
			tid2co_top[tid] = []
		tid2co_top[tid].append(datatop["x_y"][i])
	## side
	totalnum = len(dataside["nr"])
	tid2co_side = {}
	for i in range(totalnum) :
		tid = dataside["tid"][i] 
		if tid not in tid2co_side :
			tid2co_side[tid] = []
		tid2co_side[tid].append(dataside["x_y"][i])

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
			top_wb = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top wt: "))
			top_wt = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top te: "))
			top_te = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top ta: "))
			top_ta = tid2co_top[temp]
			break
		except : print("error: try again")


	# get side 
	while True :
		try : 
			temp = int(input("side wb: "))
			side_wb = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side wt: "))
			side_wt = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side te: "))
			side_te = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side ta: "))
			side_ta = tid2co_side[temp]
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
		BC = subtract(C, B)
		try :
			if x == 0 : pitchang.append(None)
			else : pitchang.append(degrees(atan(BC[1]/ BC[0])))
#			pitchang.append(atan(BC[0]/ BC[1]))
		except :
			pitchang.append(None)
		CG = BC*d/linalg.norm(BC)
		G = add(C, CG)
		I = [c+d, h]
		GI = linalg.norm(subtract(I, G))
		try : 
			flapang.append(degrees(acos((i**2 + GI**2 - g**2)/(2*i*g)))-90)
#			flapang.append(((i**2 + GI**2 - g**2)/(2*i*g)))
		except : flapang.append(None)
	return flapang, pitchang

def GetExcelDataSheet(database) : # assumes each row have same lenth, input is the excel file
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

def GetMtrackCSV(excelfile) :
	# Choose csv folder 
	folder_path = tk_GetFolderPath()
	files = listdir(folder_path)



	sheettop = excelfile.sheets["raw_data_top"]
	sheetside = excelfile.sheets["raw_data_side"]
	datatop = GetMtrackRawDataSheet(sheettop)
	dataside = GetMtrackRawDataSheet(sheetside)
	TIDtop = FindArrayInclude(datatop["tid"])
	TIDside = FindArrayInclude(dataside["tid"])

	# make TID to [x, y]
	## top
	totalnum = len(datatop["nr"])
	tid2co_top = {}
	for i in range(totalnum) :
		tid = datatop["tid"][i] 
		if tid not in tid2co_top :
			tid2co_top[tid] = []
		tid2co_top[tid].append(datatop["x_y"][i])
	## side
	totalnum = len(dataside["nr"])
	tid2co_side = {}
	for i in range(totalnum) :
		tid = dataside["tid"][i] 
		if tid not in tid2co_side :
			tid2co_side[tid] = []
		tid2co_side[tid].append(dataside["x_y"][i])

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
			top_wb = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top wt: "))
			top_wt = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top te: "))
			top_te = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top ta: "))
			top_ta = tid2co_top[temp]
			break
		except : print("error: try again")


	# get side 
	while True :
		try : 
			temp = int(input("side wb: "))
			side_wb = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side wt: "))
			side_wt = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side te: "))
			side_te = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side ta: "))
			side_ta = tid2co_side[temp]
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

def GetMtrackRawCSV(clist) : # x,y 3,4 get TID 1
	nrows = len(clist)
	Nr = []
	TID = []
	PID = []
	x_y = []
	for i in clist :
		print(i)
		Nr.append(int(i[0]))
		TID.append(int(i[1]))
		PID.append(int(i[2]))
		x_y.append([float(i[3]), float(i[4])])
	data = {
		"nr":Nr,
		"tid":TID,
		"pid":PID,
		"x_y":x_y }
	return data

def GetMtrackRawCSVdic(cdic) : # x,y 3,4 get TID 1
	nrows = len(cdic)
	Nr=i['Nr']
	TID=i['TID']
	PID=i['PID']
	x_y = []
	for i in nrows :
		for n in nrows :
			x_y.append(i['x[mm]', 'y[mm]'])
		x_y=i['']
	data = {
		"nr":Nr,
		"tid":TID,
		"pid":PID,
		"x_y":x_y }
	return data

def GetFolderPath() :
	root = gTk()
	root.withdraw()
	mypath = filedialog.askdirectory()
	return mypath

def FindCommonStringFrom0(a,b) :
	i = 0
	string = ""
	while a[i] == b[i] :
		string += a[i]
		i += 1

def GetCSVRawTopSide() :
	filepath = GetFolderPath()
	files = listdir(filepath)

	csvfiles = []
	for n in files :
		if ".csv" in n : csvfiles.append(n)
	for n in csvfiles :
		print(n)
	csvfiles.sort()

	# get file name
	print('top csv is: ')
	topcsvname = ChooseOneWithNum(csvfiles)
	print('side csv is: ')
	sidecsvname = ChooseOneWithNum(csvfiles)

	# get file as list
	with open(filepath+"/"+topcsvname, "r", encoding="ISO-8859-1") as topfile :
		# topcsvfile = csv.reader(topfile)
		topcsv = csv2list(topfile)

	with open(filepath+"/"+sidecsvname, "r", encoding="ISO-8859-1") as sidefile :
		# sidecsvfile = csv.reader(sidefile)
		sidecsv = csv2list(sidefile)
	
	csvname = FindCommonStringFrom0(topcsvname,sidecsvname)

	datatop = GetMtrackRawCSV(topcsv)
	dataside = GetMtrackRawCSV(sidecsv)

	TIDtop = FindArrayInclude(datatop["tid"])
	TIDside = FindArrayInclude(dataside["tid"])
	# make TID to [x, y]
	## top
	totalnum = len(datatop["nr"])
	tid2co_top = {}
	for i in range(totalnum) :
		tid = datatop["tid"][i] 
		if tid not in tid2co_top :
			tid2co_top[tid] = []
		tid2co_top[tid].append(datatop["x_y"][i])
	## side
	totalnum = len(dataside["nr"])
	tid2co_side = {}
	for i in range(totalnum) :
		tid = dataside["tid"][i] 
		if tid not in tid2co_side :
			tid2co_side[tid] = []
		tid2co_side[tid].append(dataside["x_y"][i])

	print("\nfind top TID: ", end = "\n")
	for i in TIDtop :	
		print(i , ": ", TIDtop[i], end = "\n")
	print("\nfind side TID: ", end = "\n")
	for i in TIDside :	
		print(i, ": ", TIDside[i], end = "\n")

	#exit() ##################

	# get top 
	while True :
		try : 
			temp = int(input("top wb: "))
			top_wb = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top wt: "))
			top_wt = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top te: "))
			top_te = tid2co_top[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("top ta: "))
			top_ta = tid2co_top[temp]
			break
		except : print("error: try again")


	# get side 
	while True :
		try : 
			temp = int(input("side wb: "))
			side_wb = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side wt: "))
			side_wt = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side te: "))
			side_te = tid2co_side[temp]
			break
		except : print("error: try again")
	while True :
		try : 
			temp = int(input("side ta: "))
			side_ta = tid2co_side[temp]
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
		"top":top_dic,
		"name":csvname
	}
	return data

def csv2list(c) :
	temp = list(c.read().split("\n"))
	clist = []
	for i in temp :
		clist.append(list(i.split(",")))
	clist.pop(0)
	# if clist[-1] == "" : clist.pop() # there is a blank string appearing at the end of the list
	clist.pop()
	return clist

