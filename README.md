# todoist-social-accountability
Using crontab, this will post an end-of-day progress report to Twitter. It could probably be repurposed for other things, as well.

# to-dos:
* Eventually, I should write a fix to clean out the links that Todoist will stuff into a task if it thinks it sees a domain name, but for now, I'm considering this finished.  (Until the links thing annoys me enough that I need to fix it.)
* Since I'm migrating away from the shitshow that is Twitter, I'm going to keep my eyes open for a Threads API.  I feel like I could migrate this pretty effectively.

# learnings:
* There's a reason the datetime and tzinfo functionality in python is as convoluted as it is -- date/time is complex, yo.
* Emoji count as multiple characters; I knew this, but I didn't _know_ this...ugh.
