import urllib.request
from datetime import date, time, datetime, timedelta, timezone
import icalendar
from dateutil import tz
from dateutil.rrule import *
import project.dash_config as dc
from project.db.models import *

def get_events(db_session):

    ec = db_session.query(EventsCache).one()
    if (datetime.now()-ec.timestamp).total_seconds() > dc.CALENDAR_CACHE_TIME:
       print('updating events cache')
       ec.data = fetch_events()
       ec.timestamp = datetime.now()
       db_session.commit()
    return ec.data

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

    return all_events




def event_is_reminder(e):
    return '#do' in e['summary']

def reminder_is_done(e):
    return '#done' in e['summary']

def get_events_from_ics(ics_string, window_start, window_end):
    
    events = []

    window_start_date = window_start.date()
    window_end_date = window_end.date()

    def finalize_event(e):
        e['is_reminder'] = event_is_reminder(e)
        e['reminder_is_done'] = e['is_reminder'] and reminder_is_done(e)

        win_start = window_start
        win_end = window_end

        if not isinstance(e['startdt'], datetime):
            win_start = window_start_date
            win_end = window_end_date
        else:
            if e['startdt'].tzinfo is None:
                win_start = datetime.fromordinal(win_start.toordinal())
                win_end = datetime.fromordinal(win_end.toordinal())            

        # don't add events that begin after window
        if e['startdt'] > win_end:
            return False

        # don't add events that end before window, except reminders
        if not (e['is_reminder'] and not e['reminder_is_done']):
            if e['enddt']:
                if e['enddt'] < win_start:
                    return False
        
        return True

    def append_event(e):

        if finalize_event(e):
            events.append(e)

    def get_recurrent_datetimes(recur_rule, start, exclusions):
        
        allday = True
        if isinstance(start, datetime):
            allday = False

        rules = rruleset()
        first_rule = rrulestr(recur_rule, dtstart=start)
        rules.rrule(first_rule)

        if not isinstance(exclusions, list):
            exclusions = [exclusions]

        for xdts in exclusions:
            if xdts is None:
                continue

            for xdt in xdts.dts:

                # dateutil rrule does not handle exdate of type DATE, so
                # hack workaround is to combine the exdate with time(0,0)
                # to make it a datetime matching what the rrule generator generates.
                # See https://github.com/dateutil/dateutil/issues/275
                if not isinstance(xdt.dt, datetime):
                    xdt.dt = datetime.combine(xdt.dt, time(0,0))
                    
                rules.exdate(xdt.dt)

        dates = []
       
        win_start = window_start
        win_end = window_end
        if not isinstance(start, datetime): # dateutil rrule expects datetime, not date
            win_start = datetime(year=win_start.year, month=win_start.month, day=win_start.day)
            win_end = datetime(year=win_end.year, month=win_end.month, day=win_end.day)
        for d in rules.between(win_start, win_end):
            # if startdt is date, truncate result to date, too.
            if allday:
                dates.append(d.date())
            else:
                dates.append(d)

        return dates


    cal = icalendar.Calendar.from_ical(ics_string)


    calevents = filter(lambda c: c.name == 'VEVENT',
        cal.walk()
        )

    def extract_ical_datetime(ical_prop):
        d = ical_prop.dt
        if getattr(d, 'tzinfo', False):
            # convent pytz timezone info to dateutil tz
            zone = tz.gettz(str(d.tzinfo))
            d=d.replace(tzinfo=zone)        

        return d

    # list of updates to instances of recurrent events
    recurrent_updates = []

    for vevent in calevents:
        summary = str(vevent.get('summary'))
        description = str(vevent.get('description'))
        location = str(vevent.get('location'))
        startdt = extract_ical_datetime(vevent.get('dtstart'))
    
        allday = False
        if not isinstance(startdt, datetime):
            allday = True
    
        enddt = None
        if not vevent.get('dtend') is None:
            enddt = extract_ical_datetime(vevent.get('dtend'))
        else:
            enddt = startdt
    
        exdate = vevent.get('exdate')
        if vevent.get('rrule'):

            reoccur = vevent.get('rrule').to_ical().decode('utf-8')
            uid = str(vevent.get('UID'))
            sequence = vevent.get('sequence')

            try:
                for d in get_recurrent_datetimes(reoccur, startdt, exdate):
                    new_e = {
                        'startdt': d,
                        'allday': allday,                  
                        'summary': summary,
                        'desc': description,
                        'loc': location,
                        'is_recurring': True,
                        'uid': uid,
                        'sequence': sequence
                        }
                    if enddt:
                        new_e['enddt'] = d + (enddt-startdt)                        
                    append_event(new_e)
            except Exception as err:
                print(err)
                print(summary)
                print(reoccur)
                print([x.dt for x in exdate.dts])
                print(startdt)
                print(isinstance(startdt,datetime))
                raise err
        else:
            new_event = {
                'startdt': startdt,
                'enddt': enddt,
                'allday': allday,
                'summary': summary,
                'desc': description,
                'loc': location,
                'is_recurring': False
                }
            
            if not vevent.get('recurrence-id'): # normal one off event
                append_event(new_event)
            else:
                new_event['recurrence-id'] = extract_ical_datetime(vevent.get('recurrence-id'))
                new_event['uid'] = str(vevent.get('uid'))
                new_event['sequence'] = vevent.get('sequence')
                new_event['is_recurring'] = True
                recurrent_updates.append(new_event)

    for e in filter(lambda x: x['is_recurring'], events):
        for update in recurrent_updates:
            if not e['startdt'] == update['recurrence-id']:
                continue
            if not e['uid'] == update['uid']:
                continue
            if not e['sequence'] <= update['sequence']:
                continue
            e.update(update)
            e['is_recurring_updated'] = True
            finalize_event(e)

    events.sort(key=lambda e: e['startdt'].timetuple())
    return events  


def get_reminders(db_session):
    all_events = get_events(db_session)

    today = date.today()
    now = datetime.now(timezone.utc)
    def is_due(e):
        if e['allday']:
            return e['startdt'] <= today and e['enddt'] > today
        else:
            return e['startdt'] <= now and e['enddt'] >= now

    def is_overdue(e):
        if e['allday']:
            return e['enddt'] <= today
        else:
            return e['enddt'] < now     


    all_reminders = list(filter(lambda e: e['is_reminder'] and not e['reminder_is_done'], all_events))

    cal_lookup = { c['name']: c for c in dc.CALENDARS }
    for e in all_reminders:
        cal=cal_lookup[e['calendar']]
        if 'reminders-text' in cal:
            e['reminders-text'] = cal['reminders-text']        
        if 'reminders-email' in cal:
            e['reminders-email'] = cal['reminders-email']        

    due = list(filter(is_due, all_reminders))
    overdue = list(filter(is_overdue, all_reminders))

    return (due, overdue)


def main():
    f = open('project/test-ics/test.ics', 'r')
    s = f.read()
    now = datetime.now(timezone.utc)
    past = now - timedelta(days=30)
    future = now + timedelta(days=10)
    events = get_events_from_ics(s, past, future)
    for e in events:
        if "pay rent" in e['summary']:
            print(e)

if __name__ == '__main__':
        main()    