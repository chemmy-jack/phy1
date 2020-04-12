import xlwings as xw
import pprint as at
import json as js
import tkinter as tk
from tkinter import filedialog
import git
import sys
import os

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

def PrintKeyWithsNum(data) :
	n = 1
	for x in data :
		key1_1 = list(data[x].keys())[0]
		key1_1_1 = list(data[x][key1_1].keys())[0]
		nrows = len(data[x][key1_1][key1_1_1])
		print("{:2} {:3} ".format(n,nrows),x)
		n += 1
	return n-1
