import pymongo
from pprint import pprint
import json 
from pymongo import MongoClient, GEO2D

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

no_hours = 0;
yes_hours = 0;
for photo in photos.find():
	data = business.find_one({'business_id':photo['business_id']})
	if data != None:
		stars = list(data.values())[9]
		longitude = list(data.values())[8]
		latitude = list(data.values())[7]
		hours = list(data.values())[14]
		business_id = list(data.values())[1]
		categories_temp = list(data.values())[13].split(',')
		categories = []
		for c in categories_temp:
			categories.append(c.strip())
		if hours is None:
			no_hours = no_hours + 1
		if hours != None :
			temp = hours.get(list(hours.keys())[0]).split("-")
			opening_time = temp[0].split(':')
			open_hours = int(opening_time[0])

			if open_hours > 12:
				open_hours = open_hours-12
			open_hours = (open_hours * 60) + int(opening_time[1])

			closing_time = temp[1].split(':')
			close_hours = int(closing_time[0])
			if close_hours > 12:
				close_hours = close_hours-12
			close_hours = (close_hours*60) + int(closing_time[1])
	
			db.photos.update_one({'business_id': photo['business_id']},{'$set': {'opening_time': int(open_hours)}}, upsert=False)
			db.photos.update_one({'business_id': photo['business_id']},{'$set': {'closing_time': int(close_hours)}}, upsert=False)
			yes_hours = yes_hours + 1
			
		db.photos.update_one({'business_id': photo['business_id']},{'$set': {'business rating': stars}}, upsert=False)
		db.photos.update_one({'business_id': photo['business_id']},{'$set': {'business id': stars}}, upsert=False)
		db.photos.update_one({'business_id': photo['business_id']},{'$set': {'loc': {'lon':float(longitude),'lat':float(latitude)}}}, upsert=False)
		db.photos.update_one({'business_id': photo['business_id']},{'$set': {'categories': categories}}, upsert=False)
		db.photos.update_one({'business_id': photo['business_id']},{'$set': {'categories': categories}}, upsert=False)

photos.create_index([("loc","2dsphere")])

# print("hours don't exist for: ", no_hours)
# print("hours exist for: ",yes_hours)

# for p in photos.find():
# 	print (p)


def user_input(input_label, input_category, input_radius, input_coordinates, input_time):
	result = []
	query = photos.find({"$and":[{'loc' : {"$geoWithin": {"$centerSphere":[input_coordinates, (input_radius/3963)]}}}, 
						{"label":{"$in":input_label}}, {"categories":{"$in":input_category}}, 
						{"opening_time":{"$lte":input_time},"closing_time":{"$gte":input_time}}]})

	for q in query:
		result.append(q['photo_id'])
	return result


input_coordinates = [-78,43]
input_radius = 3000
input_label = ["outside",'inside']
input_category = ['Seafood','Mexican','Golf']
input_time = 400
ids = user_input(input_label, input_category, input_radius, input_coordinates, input_time)
print(ids)
