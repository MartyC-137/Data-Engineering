"""How to call an API in Python
Author: Martin Palkovic
Date: 2022-01-21"""
#---------------------------------------------------------------
import requests, json

url = r'https://yoururl.com/api/work-orders'

headers = {'company-token': 'token'}

request = requests.get(url, headers = headers)#params = payload)
data = request.json()
print(request.url)
print(json.dumps(data, indent = 4, sort_keys = True)) #this returns a lot of data