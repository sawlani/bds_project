import pymongo
from pprint import pprint
import json 

client = pymongo.MongoClient("localhost", 27017)
db = client['BDAProject']
collection = db['business']
collection.drop()
with open('business.json') as f:
	for line in f:
		collection.insert_one(json.loads(line))

# query on state
cursor = collection.find({"city":"Charlotte"})

for query_result in cursor:
  print(query_result)
