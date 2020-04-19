import xlwings as xw
import tkinter as tk
from tkinter import filedialog

def tk_GetFilePath() :
	root = tk.Tk()
	root.withdraw()
	FileName = filedialog.askopenfilename()
	return FileName

point_number = 50
spec_data_path = tk_GetFilePath()
book = xw.Book(spec_data_path)
# nrows = database.sheets[2]["a1"].expand("table").rows.count 
db = book.sheets
print(type(db))
for i in db :
	print(i)
	print(db[i])
	print(i.name())
	print(db[i].name())
	
	#count each T and calculate mean T
	T = []
	for 
	name = i.name()
	reduce_raw = db[i]
	ncolumn = reduce_raw['a1'].expand("table").columns.count

	reduced = []
	with open("reduced_file.csv" ,"w") as reduced_file :
		for i in point_number :
			buff += rduced[i] + "\n"
			reduce_file.write(buff)
