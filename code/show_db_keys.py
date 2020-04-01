import json

with open ("../db/database.json", "w") as database:
	database.write(js.dumps(data, indent=4))
for x in database :
	print(x)
