# type "python -i file_name.py" to run python console after script ran
# type " exec(open("filename").read())" to execute script in python consel
import json as js

with open ("../db/rawtopside.json", "r") as database:
	data = js.loads(database.read())
for x in data :
	print(x)
