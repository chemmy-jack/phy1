import jack_functions as func 
import json as js
import jack_functions as func
import sys

# get data 
data = func.get_Jsonrawdb()

spec_data_name = func.GetSpecKeyByNum(data)

print("are u sure you want to delete", func.bcolors.WARNING, spec_data_name,func.bcolors.ENDC, "?(yes to confirm)", end = " ")

if input() == "yes" :	
	data.pop(spec_data_name, None)
	print("new key db keys:")
	func.PrintKeysWithNum(data)
	func.write_Jsondb(data)
	print("db modified")
else : print("nothing is changed")
