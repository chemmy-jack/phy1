import jack_functions as func
import xlwings as xw
import main_func as mfunc
import re # for splitting mulitply characters

print("this is the scipt to help you analyse flapping wing data of point WingBase, WingTip, TrailingEdge, Tail")

# select source of data read data 
	# jsonraw
	# excel raw sheets
	# excel data sheets

print("where to get data?")
Choosedb = func.ChooseOneWithNum("json raw top side", "excel raw top & side sheets", "excel data sheet") 

if Choosedb == "json raw top side" : 
	databasejs = func.get_Jsonrawdb()
	choosemotion = func.ChooseOneWithNum( "visualize and analyse", "visual two", "delete a data in json raw")
elif Choosedb == "excel raw top & side sheets" :
	spec_data_path = func.tk_GetFilePath()
	spec_excel_book = xw.Book(spec_data_path)
	spec_data = func.GetExcelRawTopSide(spec_excel_book)
	spec_data_Name = spec_excel_book.name
	print("you chose ",func.bcolors.FAIL, spec_excel_book.name, func.bcolors.ENDC)
	choosemotion = func.ChooseOneWithNum("write to json", "visualize and analyse", "visual two")
elif Choosedb == "excel data sheet" : 
	spec_data_path = func.tk_GetFilePath()
	spec_excel_book = xw.Book(spec_data_path)
	spec_data = func.GetExcelDataSheet(spec_excel_book)
	spec_data_Name = spec_excel_book.name
	print("you chose ",func.bcolors.FAIL, spec_excel_book.name, func.bcolors.ENDC)
	choosemotion = func.ChooseOneWithNum("write to json", "visualize and analyse", "visual two")

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
