import requests
import json
from dotenv.main import load_dotenv
import os
import tweepy
from datetime import datetime, timedelta
import pytz

# set this to your local time zone
localTimezone = "America/Chicago"

# get the .env variables
load_dotenv()

# set formats for datetime
dateFormatFull = "%Y-%m-%d %H:%M:%S"
dateFormatShort = "%Y-%m-%d"

# calculate local difference from UTC time
TIMEDIFF = datetime.utcnow().hour - datetime.now().hour
print (datetime.utcnow().hour)
print (datetime.now().hour)
print ("Timediff = " + str(TIMEDIFF))
TODAY = datetime.now().strftime(dateFormatShort)
print (TODAY)

# set up a function to change the date from GMT to local, returns a datetime object
def LocalizeTime(UTC, difference):
    out = UTC - timedelta(hours=difference)
    return out

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# Create API Object
api = tweepy.API(auth)

# set up a function to return the ID of the authenticated user's most-recent tweet, for building a whole thread of tweets, if need be

def mostRecentTweetID():
    timeline = api.user_timeline()
    return timeline[0].id

def postAsReply(statusTweet):
    api.update_status(status = statusTweet, in_reply_to_status_id = mostRecentTweetID(), auto_populate_reply_metadata=True)



# build request for Todoist SyncAPI, access token comes from .env file
url = "https://api.todoist.com/sync/v9/completed/get_all"
headers = { 'Authorization':'Bearer ' + os.environ['TODOIST_ACCESS_TOKEN'] }

# get info from Todoist and process it to a workable format
response = requests.get(url,headers=headers)
jsonPackage = response.json()

# filter down to just the items list, nothing else needed
todos = jsonPackage['items']

# prep the list for execution, count elements
for todo in todos:
    # clean up formatting on todoist's time entry, below
    todo["completed_at"] = todo["completed_at"].replace("T", " ")
    todo["completed_at"] = todo["completed_at"].replace(".000000Z", "")
    # convert the completed_at value to a local datetime object, below
    dtObject = datetime.strptime(todo["completed_at"], dateFormatFull)
    dtObject = LocalizeTime(dtObject, TIMEDIFF)
    #store the new values
    todo["completed_at_local"] = dtObject.strftime(dateFormatFull)
    todo["completed_local_date"] = dtObject.strftime(dateFormatShort)

# make a list of things that were completed today, in order
results = []
x = 0
for todo in todos:
    if todo["completed_local_date"] == TODAY:
        lineInput = "✅ " + todo["content"] + "\n"
        results.insert(0, [lineInput, len(lineInput)])
        x += 1

# inject post title in the first spot
listTitle = str(x) + " items completed today:\n"
results.insert(0, [listTitle, len(listTitle)])


# character count
tweetArray = []
charCount = 0
tweetTemp = ""

for item in results:
    if (charCount + item[1]) < 288:
        charCount = charCount + item[1]
        tweetTemp = tweetTemp + item[0]
    else: #if it doesn't fit 
        tweetTemp = tweetTemp + str(charCount)
        tweetArray.append(tweetTemp)
        charCount = 0
        tweetTemp = ""

#print (len(tweetArray))
#print (tweetArray[0])
#print (tweetArray[1])

# print(todos)