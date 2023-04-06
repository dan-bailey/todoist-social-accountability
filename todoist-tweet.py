import requests
import json
from dotenv.main import load_dotenv
import os
import tweepy
import time
from datetime import datetime, timedelta
import pytz

# get the .env variables
load_dotenv()

# set this to your local time zone
localTimezone = "America/Chicago"

# set formats for datetime
dateFormatFull = "%Y-%m-%d %H:%M:%S"
dateFormatShort = "%Y-%m-%d"

# nail down what today's local date is
TODAY = datetime.now().strftime(dateFormatShort)
print(TODAY)

# functions for shifting to local time
def makeSmartUTCObject(dumbDTObject):
    smartDT = dumbDTObject.replace(tzinfo=pytz.utc)
    return smartDT

def convertToLocalTime(smartDTObject):
    kickback = smartDTObject.astimezone(pytz.timezone(localTimezone))
    return kickback

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# Create API Object
api = tweepy.API(auth)

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
    dtObject = makeSmartUTCObject(dtObject)
    localizedTime = convertToLocalTime(dtObject)
    #store the new values
    todo["completed_at_local"] = localizedTime.strftime(dateFormatFull)
    todo["completed_local_date"] = localizedTime.strftime(dateFormatShort)


# make a list of things that were completed today, in order
results = []
x = 0
for todo in todos:
    if todo["completed_local_date"] == TODAY:
        lineInput = "✅ " + todo["content"] + "\n"
        results.insert(0, [lineInput, (len(lineInput) + 3)])
        # added a few extra characters to the count of each line to compensate for the emoji
        x += 1

# inject post title in the first spot
listTitle = str(x) + " items completed today:\n"
results.insert(0, [listTitle, len(listTitle)])


# variables for building tweets
tweetArray = []
charCount = 0
tweetTemp = ""

# build the tweets
for item in results:
    # don't do the full 280 characters, keep it a little tighter, just in case twitter counts funny
    if (charCount + item[1]) < 270:
        charCount = charCount + item[1]
        tweetTemp = tweetTemp + item[0]
    else: #if it doesn't fit
        tweetArray.append(tweetTemp)
        charCount = 0
        tweetTemp = "" + item[0]
# push the last bit into the tweet array
if (len(tweetTemp) > 0):
    tweetArray.append(tweetTemp)
    tweetTemp = ""

# error trapping 
if (len(tweetArray) == 0):
    api.update_status("✅ either the API is down, or there's an error in the script, or I did fuck-all nothing today...")

# publish the chain of stuff
maxlength = len(tweetArray)
count = 1
print (TODAY)
print ("Tweets: " + str(len(tweetArray)))
for item in tweetArray:
    print(str(len(item)))
if (len(tweetArray) >= 1):
    api.update_status(tweetArray[0])
    while (count < maxlength):
        time.sleep(2)
        timeline = api.user_timeline()
        replyID = timeline[0].id
        api.update_status(status = tweetArray[count], in_reply_to_status_id = replyID, auto_populate_reply_metadata=True)
        count += 1