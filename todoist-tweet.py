import requests
import json
import datetime

# get your own access token from developer.todoist.com
TODOIST_ACCESS_TOKEN = ""

# eventually the Twitter API access tokens will go here

# build request for Todoist SyncAPI
url = "https://api.todoist.com/sync/v9/completed/get_all"
headers = { 'Authorization':'Bearer ' + TODOIST_ACCESS_TOKEN }

# get info from Todoist and process it to a workable format
response = requests.get(url,headers=headers)
jsonPackage = response.json()

# filter down to just the items list, nothing else needed
todos = jsonPackage['items']

# cut it down to just today's stuff code goes here

# build output list
toDone = ['Today:','stuff']
print (type(toDone))

for todo in todos:
    toDone.append('✅ ' + todo.get('content'))

print(toDone)


# connect to Twitter
# post to Twitter
