import jack_functions as func
import xlwings as xw
import main_func as mfunc
import re # for splitting mulitply characters

print("this python script can read the raw front and top coordinates to json database, or visualize the coordinate of each data in the json database and export the analysed data in csv form\n")

'''
main structure :
main.py
	read and save to json database (visualize then save)
		from csv
		from xls
	visualization of data in json database
	export analysed json database in csv form
'''


print("write or read")
mode = func.ChooseOneWithNum(["write to json database", "read from json database", "deletion"])
databasejs = func.get_Jsonrawdb()

if mode == "write to json database" :
	print("what is the source?")
	source = func.ChooseOneWithNum(["csv", "xlsx"])
	if source == "csv" : # get data from csv
		spec_data = func.GetCSVRawTopSide()
		spec_data_Name = spec_data[name]
		print("you chose ",func.bcolors.FAIL, spec_data_Name, func.bcolors.ENDC)
	if source == "xlsx" :
		spec_data_path = func.tk_GetFilePath()
		spec_excel_book = xw.Book(spec_data_path)
		spec_data = func.GetExcelRawTopSide(spec_excel_book)
		spec_data_Name = spec_excel_book.name.replace(".xlsx","").replace(" ","_")
		print("you chose ",func.bcolors.FAIL, spec_excel_book.name, func.bcolors.ENDC)
	databasejs = func.get_Jsonrawdb()
	databasejs[spec_data_Name] = spec_data
	func.write_Jsondb(databasejs)
	print("visualize?")
	if input() == "n" : exit()
	else :
		o_co = func.cal_origin_coordinate(spec_data)
		mfunc.VpythonShow2(o_co, spec_data_Name)

if mode == "read from json database" :
	print("what do you wana do to the json database?")
	operatejsdb = func.ChooseOneWithNum(["old vpython visualization", "visualization", "analyse and export"])
	if operatejsdb == "old vpython visualization" :
		spec_data_Name = func.GetSpecKeyByNum(databasejs)
		spec_data = databasejs[spec_data_Name]
		func.PrintKeysWithNum(spec_data)
		o_co = func.cal_origin_coordinate(spec_data)
		mfunc.VpythonShow2(o_co, spec_data_Name)
	if operatejsdb == "visualization" :
		mfunc.VpythonShow3(databasejs) # not yet coded
	if operatejsdb ==  "analyse and export" : # export as .csv file
		AnalysedData = mfunc.VpythonAnalyseAll(databasejs) # not yet coded
		mfunc.ExportAnalysedData2CSV(AnalysedData) # not yet coded

if mode == "deletion" : # delete a data from json database
	mfunc.Deletejsonraw(databasejs)

'''
print("where to get data?")
Choosedb = func.ChooseOneWithNum(["json raw top side", "excel raw top & side sheets", "excel data sheet", "csv data"]) 

if Choosedb == "json raw top side" : 
	databasejs = func.get_Jsonrawdb()
	choosemotion = func.ChooseOneWithNum([ "visualize and analyse", "visual two", "delete a data in json raw"])
elif Choosedb == "excel raw top & side sheets" :
	spec_data_path = func.tk_GetFilePath()
	spec_excel_book = xw.Book(spec_data_path)
	spec_data = func.GetExcelRawTopSide(spec_excel_book)
	spec_data_Name = spec_excel_book.name
	print("you chose ",func.bcolors.FAIL, spec_excel_book.name, func.bcolors.ENDC)
	choosemotion = func.ChooseOneWithNum(["write to json", "visualize and analyse", "visual two"])
elif Choosedb == "excel data sheet" : 
	spec_data_path = func.tk_GetFilePath()
	spec_excel_book = xw.Book(spec_data_path)
	spec_data = func.GetExcelDataSheet(spec_excel_book)
	spec_data_Name = spec_excel_book.name
	print("you chose ",func.bcolors.FAIL, spec_excel_book.name, func.bcolors.ENDC)
	choosemotion = func.ChooseOneWithNum(["write to json", "visualize and analyse", "visual two"])
elif Choosedb == "csv data" : 
	database = func.GetCSVRawTopSide()
	choosemotion = func.ChooseOneWithNum(["write to json", "visualize and analyse", "visual two"])
	spec_data_Name = input('file name: ')

# operate with data
if choosemotion == "write to json" :
	databasejs = func.get_Jsonrawdb()
	databasejs[spec_data_Name] = spec_data
	func.write_Jsondb(databasejs)
	choosemotion = "visual two" 

if choosemotion == "visualize and analyse" :
	if Choosedb == "json raw top side" : 
		spec_data_Name = func.GetSpecKeyByNum(databasejs)
		spec_data = databasejs[spec_data_Name]
	func.PrintKeysWithNum(spec_data)
	o_co = func.cal_origin_coordinate(spec_data)
	mfunc.VpythonShow(o_co, spec_data_Name)

if choosemotion == "visual two" :
	if Choosedb == "json raw top side" : 
		spec_data_Name = func.GetSpecKeyByNum(databasejs)
		spec_data = databasejs[spec_data_Name]
	func.PrintKeysWithNum(spec_data)
	o_co = func.cal_origin_coordinate(spec_data)
	mfunc.VpythonShow2(o_co, spec_data_Name)
	
if choosemotion ==  "delete a data in json raw" :
	mfunc.Deletejsonraw(databasejs)
'''
