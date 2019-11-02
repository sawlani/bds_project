import pymongo
from pprint import pprint
import json 

client = pymongo.MongoClient("localhost", 27017)
db = client['BDAProject']
collection = db['YelpDatabase']

with open('example_1.json') as f:
	file_data = json.load(f)
	print(file_data)
collection.insert_one(file_data)
cursor = db.collection.find({"reviews.name":"testing"})
for document in cursor:
	pprint(document)

client.close()