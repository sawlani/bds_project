import pymongo
from pprint import pprint
import json
from pymongo import MongoClient
import requests
import json
import operator

photos = None
# business = None
def setup():
	print("entered")
	client = pymongo.MongoClient("localhost", 27017)
	db = client['BDAProject']
	# business_db = db['business']
	photos_db = db['photos']
	photos_db.drop()
	# business_db.drop()

	# adds business.json to database
	# with open('business.json') as f:
	# 	for line in f:
	# 		business_db.insert_one(json.loads(line))
	#
	# business_db.createIndex({"business_id": 1})
	# adds photos.json to database
	print("here")
	with open('photos_new.json') as f:
		for line in f:
			photos_db.insert_one(json.loads(line))
	print("inserted elements")
	global photos
	photos = photos_db
	# global business
	# business = business_db
	# for p in photos.find():
	# 	print (p)


def changeTime(time):
	print("time", time)
	vals = time.split(":")
	am_or_pm = vals[1][-2:]
	minutes = int(vals[1][:2])
	hours = int(vals[0])

	if am_or_pm == 'PM' and hours >= 1 and hours <= 11:
		hours = hours + 12
	time_in_minutes = (hours*60) + minutes
	# print(time_in_minutes)
	return time_in_minutes

def sort_indoor_outdoor(query, tag):
	business_wise = {}
	business_rating = {}
	business_name = {}
	for q in query:
		if str(q['label']) == tag:
			print('Here')
			if str(q['business_id']) in business_wise:
				business_wise[str(q['business_id'])].append(str(q['photo_id']))
			else:
				business_wise[str(q['business_id'])] = [str(q['photo_id'])]
				business_rating[str(q['business_id'])] = float(q['business rating'])
				business_name[str(q['business_id'])] = q['business_name'].encode('utf-8')

	sorted_business = sorted(business_rating.items(), key=operator.itemgetter(1), reverse=True)
	results = []
	labels = []
	for b in sorted_business[:5]:
		results.append(business_wise[b[0]])
		labels.append(business_name[b[0]])

	return results, labels

def user_input(input_category, input_city, input_time, output_time):

	result = []

	input_category = [str(input_category)]
	if(input_category == 'American'):
		input_category = ['American', 'American (Traditional)', 'American (New)']

	input_city = input_city.encode('utf-8')
	input_label = ["inside", "food", "outside"]

	minutes = changeTime(input_time)
	out_minutes = changeTime(output_time)

	input_time = minutes
	output_time = out_minutes

	query = photos.find({"$and":[{'city':{"$eq":input_city}},
						{"label":{"$in":input_label}}, {"categories":{"$in":input_category}},
						{"opening_time":{"$lte":input_time},"closing_time":{"$gte":output_time}}]})

	for q in query:
		result.append(q)

	asian = ["beef_tartare", "bibimbap", "dumplings", "fried_calamari", "edamame", "fried_rice", "gyoza", "hot_and_sour_soup", "miso_soup", "pad_thai", "peking_duck", "pho", "ramen", "sashimi", "seaweed_salad", "spring_rolls", "sushi", "takoyaki"]
	american = ["baby_back_ribs", "beet_salad", "caesar_salad", "caprese_salad", "chicken_wings", "clam_chowder", "club_sandwich", "crab_cakes", "deviled_eggs", "eggs_benedict", "filet_mignon", "french_fries", "grilled_cheese_sandwich", "grilled_salmon", "hamburger", "hot_dog", "lobster_roll_sandwich", "macaroni_and_cheese", "onion_rings", "pancakes", "pork_chop", "prime_rib", "pulled_pork_sandwich", "shrimp_and_grits", "steak"]
	mexican = ["breakfast_burrito", "chicken_quesadilla", "churros", "guacamole", "huevos_rancheros", "nachos", "paella", "tacos"]
	italian = ['beef_carpaccio', 'bruschetta', 'garlic_bread', 'gnocchi', 'lasagna', 'pizza', 'ravioli', 'risotto', 'spaghetti_bolognese', 'spaghetti_carbonara']
	french = ['beignet, croque_madame', 'escargots', 'foie_gras', 'french_onion_soup', 'french_toast', 'lobster_bisque']
	mediterranean = ['falafel', 'greek_salad', 'hummus']
	desserts = ['apple_pie', 'baklava', 'bread_pudding', 'cannoli', 'carrot_cake', 'cheesecake', 'chocolate_cake', 'chocolate_mousse', 'creme_brulee', 'cup_cakes', 'donuts', 'frozen_yogurt', 'ice_cream', 'macarons', 'panna_cotta', 'red_velvet_cake', 'strawberry_shortcake', 'tiramisu', 'waffles']

	dishes = {}
	dishes['Chinese'] = asian
	dishes['American'] = american
	dishes['Mexican'] = mexican
	dishes['Italian'] = italian
	dishes['French'] = french
	dishes['Mediterranean'] = mediterranean
	dishes['Desserts'] = desserts


	sorted_vals = {}
	for i in dishes.get(input_category[0]):
		sorted_vals[i] = []
	for res in result:
		if res['label'] == 'food':
			lbl = str(res['101_label'])
			temp_list = sorted_vals.get(lbl)
			if(temp_list is not None):
				temp_list.append(str(res['photo_id']))
				sorted_vals[res['101_label']] = temp_list

	count = 0
	keys = []
	values = []

	for k in sorted(sorted_vals, key=lambda k: len(sorted_vals[k]), reverse=True):
		if(count == 5):
			break
		keys.append(k)
		values.append(sorted_vals[k])
		print("length",len(sorted_vals[k]))
		count = count + 1

	print("keys", keys)
	print("values", values)


	indoors_images, indoors_labels = sort_indoor_outdoor(result, 'inside')
	outdoors_images, outdoors_labels  = sort_indoor_outdoor(result, 'outside')

	print("indoor_lables:", indoors_labels)
	print("outdoor labbls:", outdoors_labels)

	output = []
	output_labels = []
	output.append(values)
	output.append(indoors_images)
	output.append(outdoors_images)

	output_labels.append(keys)
	output_labels.append(indoors_labels)
	output_labels.append(outdoors_labels)

	id_dict = {}
	for q in result:
		id_dict[q['photo_id'].encode('utf-8')] = q

	return (output, output_labels, id_dict)

# input_coordinates = [-78,43]
# input_radius = 3000
# input_label = ['inside']
# input_category = ['Salad','Pizza']
# input_time = 0
# ids = user_input(input_label, input_category, input_radius, input_coordinates, input_time)
# print(ids)
