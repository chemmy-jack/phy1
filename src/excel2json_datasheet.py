import xlwings as xw
import json as js
import tkinter as tk
import jack_functions as func

file_name = func.tk_GetFilePath()
database = xw.Book(file_name)

add_data = GetExcelDataSheet(database)
data = get_Jsonrawdb()
print(type(data))

data[file_name] = add_data
write_Jsondb(data)
print(type(data))


