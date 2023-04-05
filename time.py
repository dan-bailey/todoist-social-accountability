from datetime import datetime, timedelta
import pytz

TIMEDIFF = datetime.utcnow().hour - datetime.now().hour
print("Time difference: " + str(TIMEDIFF))

dateFormat = "%Y-%m-%d %H:%M:%S"

timeTargetStrings = ["2023-04-04 23:14:16", "2023-04-04 23:08:58", "2023-04-04 23:08:27"]
timeTargetObjects = []

for date in timeTargetStrings:
    newDate = datetime.strptime(date, dateFormat)
    timeTargetObjects.append(newDate)

for date in timeTargetObjects:
    date = date - timedelta(hours=TIMEDIFF)

print (timeTargetObjects)