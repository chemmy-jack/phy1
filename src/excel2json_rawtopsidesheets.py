import xlwings as xw
# import numpy as np
# import matplotlib.pyplot as plt
import pprint
import json as js
import tkinter as tk
import jack_functions as func

# read data from excel file
file_name = func.tk_GetFilePath()
database = xw.Book(file_name)
data = func.GetExcelRawTopSide(database) 

for i in data :
	print(i)

data = get_Jsonrawdb()
write_Jsondb(data)
