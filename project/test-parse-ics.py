from utils.ics import *
import urllib.request
from datetime import datetime, timedelta
url = 'https://user.fm/calendar/v1-7e45ac36-f543-40af-ba49-286ca4e554e1/204dc674-4381-4994-ab56-bb0657a2df63.ics'
url = 'https://calendar.google.com/calendar/ical/49s18ffsqj06qct0vfd4gmdgkg%40group.calendar.google.com/private-3bc17ada156899bb32b45dce1bab5d8b/basic.ics'
url = 'https://calendar.google.com/calendar/ical/mqjbthtk5q5619h7541jce1480%40group.calendar.google.com/public/basic.ics'
#url = 'https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics'

with urllib.request.urlopen(url) as response:
   ics_string = response.read()

window_start = datetime.now(timezone.utc)-timedelta(days=30)
window_end = window_start + timedelta(days=60)
events = get_events_from_ics(ics_string, window_start, window_end)

for e in events:
    print('{} - {}'.format(e['startdt'], e['summary']))
