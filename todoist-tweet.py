import requests
import json
from dotenv.main import load_dotenv
import os
from datetime import datetime, timedelta

# get the .env variables
load_dotenv()

# calculate local difference from UTC time
TIMEDIFF = datetime.utcnow().hour - datetime.now().hour

# set up a function to change the date from GMT to local
def LocalizeTime(UTC, difference):
    out = UTC - timedelta(hours=difference)
    return out

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
    dateFormatFull = "%Y-%m-%d %H:%M:%S"
    dateFormatShort = "%Y-%m-%d"
    # clean up formatting on todoist's time entry, below
    todo["completed_at"] = todo["completed_at"].replace("T", " ")
    todo["completed_at"] = todo["completed_at"].replace(".000000Z", "")
    # convert the completed_at value to a local datetime object, below
    dtObject = datetime.strptime(todo["completed_at"], dateFormatFull)
    dtObject = LocalizeTime(dtObject, TIMEDIFF)
    #store the new values
    todo["completed_at_local"] = dtObject.strftime(dateFormatFull)
    todo["completed_local_date"] = dtObject.strftime(dateFormatShort)

# strip out stuff that didn't happen today


# add sort numbers to the  list of todos
# i = 1
# for todo in todos:
#    todo["sort_order"] = i
#    i+=1

# start to build output list
# toDone = ['Today:']

# connect to Twitter
# post to Twitter

print(json.dumps(todos))