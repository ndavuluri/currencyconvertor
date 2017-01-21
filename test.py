import json

json_file = "codes.json"
json_data = open(json_file)
data = json.load(json_data)
json_data.close()
codes = []
for item in data:
	codes.append(item['name']) # = str(item['code'])
for x in codes:
	print x.upper()
