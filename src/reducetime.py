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
	print('lenth =================',end = '')
	print(lenth)
	arraym = []
	ans = [0] * goal
	for n in range(lenth) :
		arraym.append(n*goal/lenth)
	for n in range(lenth-1) :
#		print('n : ' + str(n))
#		if isinstance(arraym[n], int) :
		if arraym[n].is_integer() :
			m = int(arraym[n])
			ans[m] = (array[n])
		else :
			small = arraym[n]
			big = arraym[n+1]
			smallv = array[n]
			bigv = array[n+1]
			diff = big- small
			existm = int(big)-int(small)
			for x in range(existm) :
				m = int(small) + x + 1
				dbig = big - m
				dsmall = m - small
				ans[m] = ((smallv*dbig/diff+bigv*dsmall/diff))
#				print(str(m) + '========= ans : ===============' + str(ans[m]))
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
	print(count)
	
	#count each T and calculate mean T
	T = []
	name = db[i].name
	print(name)
	ncolumn.append(db[i]['a2'].expand("table").columns.count)
	print(db[i].range('a1').expand('table').columns)
	val_tmp = [] # list of value in each element
	print(ncolumn[count])
	for x in range(ncolumn[count]) : # finnish val_temp value placing
		alpha = chr(ord('a')+x)
		nrows = db[i][alpha +'1'].expand("table").rows.count
		temp = db[i][:nrows, x].value
		temp.pop(0) #note : because data start at second
		val_tmp.append(temp)
		T.append(nrows-1)#note : because data start at second
	mT = (st.mean(T)) # meanT calculated
	val_temp1 = []
	for i in val_tmp : # calculate reduced list of each element in val_temp
		print('============================')
		val_temp1.append(calcreduce(i, point_number))
	val_temp2 = [] # reduced list
	for x in range(point_number) : # finnish reduced number
		temp = []
		for i in range(ncolumn[count]) :
			temp.append(val_temp1[i][x])
		val_temp2.append(st.mean(temp))
	buf = [name,mT]
	buf += val_temp2
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
