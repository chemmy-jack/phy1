import jack_functions as func
import xlwings as xw
import VpythonShow_tobeimport as vshowfunc

print("this is the scipt to help you analyse flapping wing data of point WingBase, WingTip, TrailingEdge, Tail")

# select source of data read data 
	# jsonraw
	# excel raw sheets
	# excel data sheets

print("where to get data?")
Choosedb = func.ChooseOneWithNum("json raw top side", "excel raw top & side sheets", "excel data sheet") 

if Choosedb == "json raw top side" : 
	databasejs = func.get_Jsonrawdb()
	choosemotion = func.ChooseOneWithNum( "visualize and analyse")
elif Choosedb == "excel raw top & side sheets" :
	spec_data_name = func.tk_GetFileName()
	database = xw.Book(spec_data_name)
	spec_data = func.GetExcelRawTopSide(database)
	choosemotion = func.ChooseOneWithNum("write to json", "visualize and analyse")
elif Choosedb == "excel data sheet" : 
	spec_data_name = func.tk_GetFileName()
	database = xw.Book(spec_data_name)
	spec_data = func.GetExcelDataSheet(database)
	choosemotion = func.ChooseOneWithNum("write to json", "visualize and analyse")

# operate with data
if choosemotion == "write to json" :
	databasejs = func.get_Jsonrawdb()
	databasejs[spec_data_name] = spec_data
	func.write_Jsondb(databasejs)
if choosemotion == "visualize and analyse" :
	if Choosedb == "json raw top side" : 
		spec_data_name = func.GetSpecKeyByNum(databasejs)
		spec_data = databasejs[spec_data_name]
	func.PrintKeysWithNum(spec_data)
	o_co = func.cal_origin_coordinate(spec_data)
	vshowfunc.VpythonShow(o_co, spec_data_name)
	
