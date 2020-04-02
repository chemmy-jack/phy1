def cal_origin_coordinate(spec_data) :
	# check same lenth of rows
	key1 = list(spec_data.keys())[0]
	key1_1 = list(spec_data[key1].keys())[0]
	nrows = len(spec_data[key1][key1_1])
	for x in spec_data :
		for y in spec_data[x] :
			print("{:4}".format(x),end=" ")
			print("{:15}".format(y),end=" ")
			print(len(spec_data[x][y]))
			# if len(y) != nrows :return print("error: row lenth not the same")
	o_wb = []
	o_wt = []
	o_te = []
	o_ta = []
	for i in range(nrows):
		o_wb.append([-(spec_data["side"]["wing_base"][i][0] + spec_data["top"]["wing_base"][i][0]) / 2, spec_data["side"]["wing_base"][i][1], -spec_data["top"]["wing_base"][i][1]])
		o_wt.append([-(spec_data["side"]["wing_tip"][i][0] + spec_data["top"]["wing_tip"][i][0]) / 2, spec_data["side"]["wing_tip"][i][1], -spec_data["top"]["wing_tip"][i][1]])
		o_te.append([-(spec_data["side"]["trailing_edge"][i][0] + spec_data["top"]["trailing_edge"][i][0]) / 2, spec_data["side"]["trailing_edge"][i][1], -spec_data["top"]["trailing_edge"][i][1]])
		o_ta.append([-(spec_data["side"]["tail"][i][0] + spec_data["top"]["tail"][i][0]) / 2, spec_data["side"]["tail"][i][1], -spec_data["top"]["tail"][i][1]])
	return { "wb":o_wb, "wt":o_wt, "te":o_te, "ta":o_ta}
# a comment

