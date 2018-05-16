from datetime import date, datetime, timedelta
import icalendar
from dateutil import tz
from dateutil.rrule import *

def event_is_reminder(e):
    return '#do' in e['summary']

def reminder_is_done(e):
    return '#done' in e['summary']

def get_events_from_ics(ics_string, window_start, window_end):
    
    events = []

    window_start_date = window_start.date()
    window_end_date = window_end.date()

    def append_event(e):

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
            return

        # don't add events that end before window, except reminders
        if not (e['is_reminder'] and not e['reminder_is_done']):
            if e['enddt']:
                if e['enddt'] < win_start:
                    return

        events.append(e)

    def get_recurrent_datetimes(recur_rule, start, exclusions):
        rules = rruleset()
        first_rule = rrulestr(recur_rule, dtstart=start)
        rules.rrule(first_rule)
        if not isinstance(exclusions, list):
            exclusions = [exclusions]

        for xdt in exclusions:
            try:
                rules.exdate(xdt.dt)
            except AttributeError:
                pass

        dates = []
       
        win_start = window_start
        win_end = window_end
        if not isinstance(start, datetime):
            win_start = datetime(year=win_start.year, month=win_start.month, day=win_start.day)
            win_end = datetime(year=win_end.year, month=win_end.month, day=win_end.day)
        for d in rules.between(win_start, win_end):
            dates.append(d)
        return dates


    cal = icalendar.Calendar.from_ical(ics_string)


    calevents = filter(lambda c: c.name == 'VEVENT',
        cal.walk()
        )


    for vevent in calevents:
        summary = str(vevent.get('summary'))
        description = str(vevent.get('description'))
        location = str(vevent.get('location'))
        startdt = vevent.get('dtstart').dt
    
        allday = False
        if not isinstance(startdt, datetime):
            allday = True
    
        enddt = None
        if not vevent.get('dtend') is None:
            enddt = vevent.get('dtend').dt
        else:
            enddt = startdt
    
        if getattr(startdt, 'tzinfo', False):
            # convent pytz timezone info to dateutil tz
            zone = tz.gettz(str(startdt.tzinfo))
            startdt=startdt.replace(tzinfo=zone)

        if getattr(enddt, 'tzinfo', False):
            # convent pytz timezone info to dateutil tz
            zone = tz.gettz(str(enddt.tzinfo))
            enddt=enddt.replace(tzinfo=zone)


        exdate = vevent.get('exdate')
        if vevent.get('rrule'):

            reoccur = vevent.get('rrule').to_ical().decode('utf-8')
            for d in get_recurrent_datetimes(reoccur, startdt, exdate):
                new_e = {
                    'startdt': d,      
                    'allday': allday,                  
                    'summary': summary,
                    'desc': description,
                    'loc': location
                    }
                if enddt:
                    new_e['enddt'] = d + (enddt-startdt)                        
                append_event(new_e)
        else:
            append_event({
                'startdt': startdt,
                'enddt': enddt,
                'allday': allday,
                'summary': summary,
                'desc': description,
                'loc': location
                })

    events.sort(key=lambda e: e['startdt'].timetuple())
    return events
