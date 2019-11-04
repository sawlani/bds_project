import pymongo
from pprint import pprint
import json 

client = pymongo.MongoClient("localhost", 27017)
db = client['BDAProject']
business = db['business']
photos = db['photos']
business.drop()
photos.drop()

# adds business.json to database
with open('business.json') as f:
	for line in f:
		business.insert_one(json.loads(line))

# adds photos.json to database
with open('photo.json') as f:
	for line in f:
		photos.insert_one(json.loads(line))

# simple query on state
cursor = business.find({"city":"Charlotte"})

# adds business rating field to every photo
for p in photos.find():
	db.photos.update_one({'_id': p['_id']},{'$set': {'business rating': -1}}, upsert=False)


# updates business rating acordingly in photos
for photo in photos.find():
	data = business.find_one({'business_id':photo['business_id']})
	if data != None:
		stars = list(data.values())[9]
		print(stars)
		db.photos.update_one({'business_id': photo['business_id']},{'$set': {'business rating': stars}}, upsert=False)

# loop through photos and check that update was successfull 
for p in photos.find():
	print (p)