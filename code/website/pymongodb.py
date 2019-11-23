import pymongo
from pprint import pprint
import json
from pymongo import MongoClient, GEO2D
import requests
import json


def setup():
	client = pymongo.MongoClient("localhost", 27017)
	db = client['BDAProject']
	business = db['business']
	photos = db['photos']
	business.drop()
	photos.drop()

	# adds business.json to database
	with open('business_small.json') as f:
		for line in f:
			business.insert_one(json.loads(line))

	# adds photos.json to database
	with open('photo_small.json') as f:
		for line in f:
			photos.insert_one(json.loads(line))
	print("inserted elements")
	business.create_index([("business_id",1)])
	no_hours = 0;
	yes_hours = 0;
	num_photo = 0
	num_matched = 0
	for photo in photos.find():
		# print("photo_num",num_photo)
		num_photo = num_photo + 1
		data = business.find_one({'business_id':photo['business_id']})
		if data != None:
			# print("here")
			# print("matched_num",num_matched)
			num_matched = num_matched + 1
			stars = data.get('stars')
			longitude = data.get('longitude')
			latitude = data.get('latitude')
			hours = data.get('hours')
			business_id = data.get('business_id')
			categories_temp = data.get('categories').split(',')
			categories = []
			for c in categories_temp:
				categories.append(c.strip())
			if hours is None:
				no_hours = no_hours + 1
			if hours != None :
				temp = hours.get(list(hours.keys())[0]).split("-")
				opening_time = temp[0].split(':')
				open_hours = int(opening_time[0])
				#
				# if open_hours > 12:
				# 	open_hours = open_hours-12
				open_hours = (open_hours * 60) + int(opening_time[1])

				closing_time = temp[1].split(':')
				close_hours = int(closing_time[0])
				# if close_hours > 12:
				# 	close_hours = close_hours-12
				close_hours = (close_hours*60) + int(closing_time[1])

				db.photos.update_one({'business_id': photo['business_id']},{'$set': {'opening_time': int(open_hours),'closing_time': int(close_hours)}},upsert=False)
				yes_hours = yes_hours + 1
			coord = [float(longitude), float(latitude)]
			db.photos.update_one({'business_id': photo['business_id']},{'$set': {'business rating': stars, 'business id': stars, 'categories': categories,
								'loc': {'coordinates':coord, 'type':"Point"}}}, upsert=False)


	photos.create_index([("loc","2dsphere")])

	print("hours don't exist for: ", no_hours)
	print("hours exist for: ",yes_hours)
	#
	for p in photos.find():
		print (p)

	return photos

def user_input(input_label, input_category, input_radius, input_time, output_time):
	result = []
	photos = setup()
	# send_url = 'http://freegeoip.net/json'
	# r = requests.get(send_url)
	# j = json.loads(r.text)
	# lat = j['latitude']
	# lon = j['longitude']
	input_category = [str(input_category)]
	input_radius = float(str(input_radius))
	input_time = str(input_time)
	print("orig in", input_time)
	print("orin out", output_time)
	print("cat",input_category)
	print("rad",input_radius)

	minutes = changeTime(input_time)
	out_minutes = changeTime(output_time)
	#
	input_time = minutes
	output_time = out_minutes
	print("input_time",input_time)
	print("output_time", output_time)
	input_coordinates = [-80, 35]
	input_label = ['inside']
	query = photos.find({"$and":[{'loc' : {"$nearSphere": {"$geometry":{"coordinates":input_coordinates, "type":"Point"},
						"$minDistance":1, "$maxDistance":((input_radius*10)/3963)}}},
						{"label":{"$in":input_label}}, {"categories":{"$all":input_category}},
						{"opening_time":{"$lte":input_time},"closing_time":{"$gte":output_time}}]})

	for q in query:
		result.append(q['photo_id'])

	return result


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
# input_coordinates = [-78,43]
# input_radius = 3000
# input_label = ['inside']
# input_category = ['Salad','Pizza']
# input_time = 0
# ids = user_input(input_label, input_category, input_radius, input_coordinates, input_time)
# print(ids)
