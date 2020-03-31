import json as js
# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = js.loads(x)

# the result is a Python dictionary:
print(y["age"])
print(y)
print(x)
f = open("test.json", "r+")

temp = js.loads(f.read())
print(f)
print(temp)
f.close()

fil = open("test1.json", "a+")
fil.write(js.dumps(temp, indent=2))
print(fil.read())
print(js.dumps(temp))
fil.close

