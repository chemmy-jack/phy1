import sys
from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter import filedialog
import csv

sys.path.append('../src/')
import jack_functions as func 

def GetMtrackRawCSV(clist) : # x,y 3,4 get TID 1
	nrows = len(clist)
	Nr = []
	TID = []
	PID = []
	x_y = []
	for i in nrows :
		Nr.append(i[0])
		TID.append(i[1])
		PID.append(i[2])
		x_y.append([i[3], i[3]])
	data = {
		"nr":Nr,
		"tid":TID,
		"pid":PID,
		"x_y":x_y }
	return data

def GetFolderPath() :
	root = tk.Tk()
	root.withdraw()
	mypath = filedialog.askdirectory()
	return mypath

def GetCSVRawTopSide() :
	filepath = GetFolderPath()
		files = listdir(filepath)

	csvfiles = []
	for n in files :
		if ".csv" in n : csvfiles.append(n)
	for n in csvfiles :
		print(n)

	# get file name
	print('top csv is: ')
	topcsvname = ChooseOneWithNum(csvfiles)
	print('side csv is: ')
	sidecsvname = ChooseOneWithNum(csvfiles)


	# get file as list
	with open(maypath+topcsvname, "r") as topfile :
		topcsv = csv.reader(topfile)

	with open(maypath+sidecsvname, "r") as sidefile :
		sidecsv = csv.reader(sidefile)

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

