import pymongo
from pprint import pprint
import json
from pymongo import MongoClient
import requests
import json

photos = None
def setup():
	print("entered")
	client = pymongo.MongoClient("localhost", 27017)
	db = client['BDAProject']
	# business = db['business']
	photos_db = db['photos']
	# business.drop()
	photos_db.drop()

	# adds business.json to database
	# with open('business_small.json') as f:
	# 	for line in f:
	# 		business.insert_one(json.loads(line))

	# adds photos.json to database
	print("here")
	with open('photos_new.json') as f:
		for line in f:
			photos_db.insert_one(json.loads(line))
	print("inserted elements")
	photos = photos_db
	# for p in photos.find():
	# 	print (p)


def changeTime(time):
	print("time", time)
	vals = time.split(":")
	am_or_pm = vals[1][-2:]
	minutes = int(vals[1][:2])
	hours = int(vals[0])
	# print("valss", vals)
	#
	print("ampm", am_or_pm)
	print("hours", hours)
	if am_or_pm == 'PM' and hours >= 1 and hours <= 11:
		hours = hours + 12
	time_in_minutes = (hours*60) + minutes
	# print(time_in_minutes)
	return time_in_minutes

def user_input(input_category, input_city, input_time, output_time):
	for p in photos.find():
		print (p)
	result = []
	# send_url = 'http://freegeoip.net/json'
	# r = requests.get(send_url)
	# j = json.loads(r.text)
	# lat = j['latitude']
	# lon = j['longitude']
	input_category = [str(input_category)]
	# input_radius = float(str(input_radius))
	# input_time = str(input_time)
	input_city = str(input_city)
	input_label = ["inside", "food", "outside"]
	# print("orig in", input_time)
	# print("orin out", output_time)
	# print("cat",input_category)
	# print("rad",input_radius)

	minutes = changeTime(input_time)
	out_minutes = changeTime(output_time)
	#
	input_time = minutes
	output_time = out_minutes
	print("input_time",input_time)
	print("output_time", output_time)
	print("input_category", input_category)
	print("input_city", input_city)
	print("input_label", input_label)

	# input_coordinates = [-80, 35]
	# input_label = ['inside']
	query = photos.find({"$and":[{'city':{"$eq":input_city}},
						{"label":{"$in":input_label}}, {"categories":{"$all":input_category}},
						{"opening_time":{"$lte":input_time},"closing_time":{"$gte":output_time}}]})

	for q in query:
		result.append(q['photo_id'])

	return result

# input_coordinates = [-78,43]
# input_radius = 3000
# input_label = ['inside']
# input_category = ['Salad','Pizza']
# input_time = 0
# ids = user_input(input_label, input_category, input_radius, input_coordinates, input_time)
# print(ids)
