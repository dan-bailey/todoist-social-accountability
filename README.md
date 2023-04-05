# Todoist-Social-Accountability
Using crontab, this will post an end-of-day progress report to Twitter. It could probably be repurposed for other things, as well.

# To-dos:
* Hah, figured out why this breaks after a certain time of day -- after midnight, subtracting the difference between the local hour and UTC hour, yields -19 (instead of 5), and subtracting -19 sends my dates for task completions flying off into the future!  I'll fix this tomorrow.
* Actually post the tweets/threads, yo.  (Already prototyped and tested, just need to integrate.)

# Learnings:
* Todoist is great but their API drives me batshit crazy
* there's got to be a better way to handle datetime operations in python
