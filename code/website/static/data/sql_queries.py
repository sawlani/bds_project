import sqlite3

def choropleth_query(census_tracts = [],start_year=2019,end_year=2030,bathroom_start=0,bathroom_end=15,
	bedroom_start=0,bedroom_end=15,land_area_start=0,land_area_end=1000000,price_start=0,price_end=1e6):
	conn = sqlite3.connect('static/data/aggregated_data.db')
	cur = conn.cursor()
	if census_tracts == []:
		sql = "SELECT CENSUS_TRACT, AVG((`{1}`-`{0}`)/(`{0}`)*100) as returns FROM Properties WHERE BATHRM>{3} and BATHRM<{4} and BEDRM>{5} and BEDRM<{6} and LANDAREA>{7} and LANDAREA<{8} and `{0}`>{9} and `{1}`<{10} GROUP BY CENSUS_TRACT".format(start_year,end_year,census_tracts,bathroom_start,bathroom_end,bedroom_start,bedroom_end,land_area_start,land_area_end,price_start,price_end)
	else:
		sql = "SELECT CENSUS_TRACT, AVG((`{1}`-`{0}`)/(`{0}`)*100) as returns FROM Properties WHERE CENSUS_TRACT IN ({11}) and BATHRM>{3} and BATHRM<{4} and BEDRM>{5} and BEDRM<{6} and LANDAREA>{7} and LANDAREA<{8} and `{0}`>{9} and `{1}`<{10} GROUP BY CENSUS_TRACT".format(start_year,end_year,census_tracts,bathroom_start,bathroom_end,bedroom_start,bedroom_end,land_area_start,land_area_end,price_start,price_end, ",".join(map(str, census_tracts)))
	result = cur.execute(sql).fetchall()
	dict = {int(res[0]): res[1] for res in result}
	return dict

def census_tract_data(census_tract = 4801,start_year=2019,end_year=2030,bathroom_start=0,bathroom_end=15,bedroom_start=0,
	bedroom_end=15,land_area_start=0,land_area_end=1000000,price_start=0,price_end=1e6):
	conn = sqlite3.connect('static/data/aggregated_data.db')
	cur = conn.cursor()
	years = range(int(start_year), int(end_year)+1)
	sql = "SELECT CENSUS_TRACT, {12} FROM Properties WHERE CENSUS_TRACT= {11} and BATHRM>{3} and BATHRM<{4} and BEDRM>{5} and BEDRM<{6} and LANDAREA>{7} and LANDAREA<{8} and `{0}`>{9} and `{1}`<{10}".format(start_year,end_year,census_tract,bathroom_start,bathroom_end,bedroom_start,bedroom_end,land_area_start,land_area_end,price_start,price_end, census_tract, ",".join(("`"+str(n)+"`" for n in years)))
	result=cur.execute(sql).fetchall()
	print(result)
	dict = {int(res[0]): {years[i-1]: res[i] for i in range(1, len(res))} for res in result}
	return dict


def portfolio_query(census_tracts = [],start_year=2019,end_year=2030,bathroom_start=0,bathroom_end=15,bedroom_start=0,
	bedroom_end=15,land_area_start=0,land_area_end=1000000,price_start=0,price_end=1e6,total_budget=1e7):
	conn = sqlite3.connect('static/data/aggregated_data.db')
	cur = conn.cursor()
	if census_tracts == []:
		sql = "SELECT `{0}`, (`{1}`-`{0}`)/(`{0}`)*100 as returns, * FROM Properties WHERE BATHRM>{3} and BATHRM<{4} and BEDRM>{5} and BEDRM<{6} and LANDAREA>{7} and LANDAREA<{8} and `{0}`>{9} and `{1}`<{10} ORDER BY returns DESC".format(start_year,end_year,census_tracts,bathroom_start,bathroom_end,bedroom_start,bedroom_end,land_area_start,land_area_end,price_start,price_end)
	# else:
	# 	sql = "SELECT `{0}`,(`{1}`-`{0}`)/(`{0}`)*100 as returns,* FROM Properties WHERE CENSUS_TRACT in ({11}) and BATHRM>{3} and BATHRM<{4} and BEDRM>{5} and BEDRM<{6} and LANDAREA>{7} and LANDAREA<{8} and `{0}`>{9} and `{1}`<{10} ORDER BY returns DESC".format(start_year,end_year,census_tract,bathroom_start,bathroom_end,bedroom_start,bedroom_end,land_area_start,land_area_end,price_start,price_end, census_tract, ",".join(("`"+str(n)+"`" for n in range(start_year,end_year+1))))

	result=cur.execute(sql).fetchall()
	names_dict = {cur.description[i][0]: i for i in range (0, len(cur.description))}
	years = range(int(start_year), int(end_year)+1)

	budget=0
	count=0
	total_budget = float(total_budget)
	while budget<total_budget and count<len(result):
		# print(budget<total_budget)
		# print(total_budget)
		budget+=result[count][0]
		count+=1

	# print(len(result))
	result=result[:count]

	best_years = []
	for i in range(0, len(result)):
		max_price = float("-inf")
		best_year = None
		for year in years:
			y = str(year)
			price = result[i][names_dict[y]]
			if(price > max_price):
				max_price = price
				best_year = y
		best_years.append(best_year)

	return result, names_dict, best_years