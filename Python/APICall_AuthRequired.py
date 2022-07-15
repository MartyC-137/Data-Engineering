"""How to call an API when authorization is required
Author: Martin Palkovic
Date: 2022-01-21"""


#authorization

#--------------------------------------------------------------
import requests, json, os

base_url = r'https://yoururl.com'
creds = {'username':'username',
           'password':'password'}
post = requests.post(base_url, data = creds)
token = post.json()
token = ''.join([str(v) for k,v in token.items()])
# print(token)

"""Post authorization"""
url = os.path.join(base_url, 'companies').replace('\\', '/')
companies = requests.get(url, headers = {'Authorization': '{}'.format(token)})
data = companies.json()
# print(companies.url)
# print(data)

"""get request"""
url = r'https://yoururl.com/inspections'
payload = {'showevent': 'false',
           'start': '2021-11-01',
           'end': '2021-12-01',
           'showonlycompleted': 'false'}
           
request = requests.get(url, params = payload, headers = {'Authorization': '{}'.format(token)})
final = request.json()
print(request.url)
print(json.dumps(final, indent = 4, sort_keys = True))