import requests
import json
from dotenv.main import load_dotenv
import os

import datetime
from dateutil import tz

# lockdown what today's date is in the local time zone
TODAY = datetime.date.today()
print (TODAY)

# get the .env variables
load_dotenv()



# calculate difference between GMT and local time


# eventually set up a function to change the date from GMT to local
def localizeDate(originalTime, timeDiff):
    localizedTime = 0
    return localizedTime


# build request for Todoist SyncAPI, access token comes from .env file
url = "https://api.todoist.com/sync/v9/completed/get_all"
headers = { 'Authorization':'Bearer ' + os.environ['TODOIST_ACCESS_TOKEN'] }


# get info from Todoist and process it to a workable format
response = requests.get(url,headers=headers)
jsonPackage = response.json()

# filter down to just the items list, nothing else needed
todos = jsonPackage['items']

# prep the list for execution
for todo in todos:
    todo["completed_at"] = todo["completed_at"].replace("T", " ")
    todo["completed_at"] = todo["completed_at"].replace(".000000Z", "")
    todo["localized_completion"] = localizeDate(todo["completed_at"], -8)

# strip out stuff that didn't happen today


# add sort numbers to the  list of todos
i = 1
for todo in todos:
    todo["sort_order"] = i
    i+=1

# start to build output list
# toDone = ['Today:']

# connect to Twitter
# post to Twitter

# print(json.dumps(todos))