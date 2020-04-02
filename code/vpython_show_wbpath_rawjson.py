from vpython import *
import json as js
import jack_functions as func
import sys

print("getting data from ../db/rawtopside.json")
with open ("../db/rawtopside.json", "r") as database:
    data = js.loads(database.read())
print("finnish reading data")

n = 1
# print possibles
for x in data :
	key1_1 = list(data[x].keys())[0]
	key1_1_1 = list(data[x][key1_1].keys())[0]
	nrows = len(data[x][key1_1][key1_1_1])
	print("{:2} {:3} ".format(n,nrows),x)
	n += 1
n -= 1
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
		spec_data = data[x]
		print(x)
		break
o_co = func.cal_origin_coordinate(spec_data)

