from datetime import datetime
import pytz

localFormat = "%Y-%m-%d %H:%M:%S"
localTimezone = "America/Chicago"

def makeSmartUTCObject(dumbDTObject):
    smartDT = dumbDTObject.replace(tzinfo=pytz.utc)
    return smartDT

def convertToLocalTime(smartDTObject):
    kickback = smartDTObject.astimezone(pytz.timezone(localTimezone))
    return kickback

utcs = [
"2023-04-05 14:30:10",
"2023-04-05 15:30:10",
"2023-04-05 16:30:10",
"2023-04-05 17:30:10",
"2023-04-05 18:30:10",
"2023-04-05 19:30:10",
"2023-04-05 20:30:10",
"2023-04-05 21:30:10",
"2023-04-05 22:30:10",
"2023-04-05 23:30:10",
"2023-04-06 00:30:10",
"2023-04-06 01:30:10",
"2023-04-06 02:30:10"
]

count = 0
while (count < 13):
    target = datetime.strptime(utcs[count], localFormat)
    a = makeSmartUTCObject(target)
    b = convertToLocalTime(a)
    print("UTC: " + a.strftime(localFormat))
    print("Local: " + b.strftime(localFormat))
    print(" ")
    count += 1


