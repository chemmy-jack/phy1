import jack_functions as func 
import json as js
import jack_functions as func

# get data 
data = func.get_Jsonrawdb()

spec_data_name = func.GetSpecKeyByNum(data)

print("are u sure you want to delete", func.bcolors.WARNING, spec_data_name,func.bcolors.ENDC, "?(yes to confirm)", end = " ")
# print possibles
n = func.PrintKeysWithNum(data)

# choose specfic
N = input("type number of file to see track: ")
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
		print(x)
		break
if input() == "yes" :	
	data.pop(spec_data_name, None)
	print("new key db keys:")
	func.PrintKeysWithNum(data)
	write_Jsondb(data)
	print("db modified")
else : print("nothing is changed")
