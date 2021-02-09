import json

with open('Punta Delicia.txt','r') as json_file:
    data = json.load(json_file)


print(json.dumps(data, indent=1))