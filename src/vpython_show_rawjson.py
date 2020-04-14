from vpython import *
import json as js
import jack_functions as func
import sys
import numpy as np
import VpythonShow_tobeimport as vshowfunc

# get data 
data = func.get_Jsonrawdb()
spec_data_name = func.GetSpecKeyByNum(data)
spec_data = data[spec_data_name]
o_co = func.cal_origin_coordinate(spec_data)
vshowfunc.VpythonShow(o_co, spec_data_name)
