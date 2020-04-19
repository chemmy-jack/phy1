import xlwings as xw
import tkinter as tk
from tkinter import filedialog
import statistics as st

def tk_getfilepath() :
	root = tk.Tk()
	root.withdraw()
	filepath = filedialog.askopenfilename()
	return filepath

def calcreduce(array, goal) :
	lenth = len(array)
	arraym = []
	ans = [0] * goal
	for n in range(lenth) :
		arraym.append(n*goal/lenth)
	for n in range(lenth-1) :
		if isinstance(arraym[n], int) :
			m = arraym[n]
			ans[m] = (array[n])
		else :
			small = arraym[n]
			big = arraym[n+1]
			smallv = array[n]
			bigv = array[n+1]
			diff = big-small
			existm = int(big)-int(small)
			print(existm)
			for x in range(existm) :
				m = int(small) + x
				dbig = big - m
				dsmall = m - small
				ans[m] = ((smallv*dbig/diff+bigv*dsmall/diff))
				print(m)
	return ans

point_number = 50
spec_data_path = tk_getfilepath()
book = xw.Book(spec_data_path)
# nrows = database.sheets[2]["a1"].expand("table").rows.count 
db = book.sheets
val = []
ncolumn = []
print(type(db))
count = 0 
for i in db :
	print(i)
	print(db[i])
	
	#count each T and calculate mean T
	T = []
	name = db[i].name
	print(name)
	ncolumn.append(db[i]['a1'].expand("table").columns.count)
	val_tmp = []
	for x in range(ncolumn[count]) :
		alpha = chr(ord('a')+x)
		nrows = db[i][alpha +'1'].expand("table").rows.count
		temp = db[i][:nrows, x].value
		temp.pop(0) #note : because data start at second
		val_tmp.append(temp)
		T.append(nrows-1)#note : because data start at second
	mT = (st.mean(T)) # meanT appended
	buf = [name,mT]
	buf += calcreduce(val_tmp, point_number)
	val.append(buf)
	count += 1



with open("reduced_file.csv" ,"w") as reduced_file :
	buff = ""
	print(len(val[0]))
	print(len(val))
	for x in range(len(val[0])) :
		for i in range(len(val)) :
			buff += str(val[i][x]) + ","
		buff += "\n"
	reduced_file.write(buff)
