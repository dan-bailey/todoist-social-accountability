# Todoist-Social-Accountability
Using crontab, this will post an end-of-day progress report to Twitter. It could probably be repurposed for other things, as well.

# To-dos:
* Eventually, I should write a fix to clean out the links that Todoist will stuff into a task if it thinks it sees a domain name, but for now, I'm considering this finished.  (Until the links thing annoys me enough that I need to fix it.)

# Learnings:
* there's a reason the datetime and tzinfo functionality in python is as convoluted as it is -- date/time is complex, yo
* there's got to be a better way to handle datetime operations in python
* emoji count as multiple characters; I knew this, but I didn't _know_ this...ugh
