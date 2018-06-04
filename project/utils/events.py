from project.utils.ics import get_events_from_ics
import urllib.request
from datetime import datetime, timedelta, timezone

try:
    import project.dash_config as dc
except ModuleNotFoundError as e:
    import project.dash_config_default as dc


def get_events():
    return fetch_events()

def fetch_events():
    all_events = []
    for cal in dc.CALENDARS:

        with urllib.request.urlopen(cal['url']) as response:
           ics_string = response.read()

        now = datetime.now(timezone.utc)
        past = now - timedelta(days=30)
        future = now + timedelta(days=30)
        events = get_events_from_ics(ics_string, past, future)
        for e in events:
            e['calendar']=cal['name']
            e['color']=cal['color']

        all_events += events

    def sortkey(e):
        if isinstance(e['startdt'], datetime):
            return e['startdt'].utctimetuple()
        else:
            return e['startdt'].timetuple()


    all_events.sort(key=sortkey)

    for e in all_events:
        # since flask jsonify doesn't handle tz, convert explicitly:
        e['startdt']=e['startdt'].isoformat()
        if e['enddt']:
            e['enddt']=e['enddt'].isoformat()

    return all_events