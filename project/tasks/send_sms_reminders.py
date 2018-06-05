from twilio.rest import Client
import project.utils.events as events
import project.dash_config as dc
from project.db.models import *
from project.db import make_session
from datetime import date, datetime, timedelta, timezone

account_sid = dc.TWILIO['account-sid']
auth_token = dc.TWILIO['auth-token']
phone_number = dc.TWILIO['phone-number']

def send(to, body):
	client = Client(account_sid, auth_token)
	message = client.messages.create(body=body, from_=phone_number, to=to)


s = make_session()

all_events = events.get_events(s)

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

due = list(filter(is_due, all_reminders))
overdue = list(filter(is_overdue, all_reminders))


print('All:')
print([e['summary'] for e in all_reminders])
print('Due:')
print([e['summary'] for e in due])
print('')
print('Overdue:')
print([e['summary'] for e in overdue])

cal_lookup = { c['name']: c for c in dc.CALENDARS }

for e in overdue:
	body = "! " + e['summary'].replace('#do', '').strip()
	body=body[0:160]
	cal=cal_lookup[e['calendar']]
	if 'reminders-text' in cal:
		numbers = cal['reminders-text']
		for to in numbers:
			send(to, body)

for e in due:
	body = e['summary'].replace('#do', '').strip()
	body=body[0:100]
	cal=cal_lookup[e['calendar']]
	if 'reminders-text' in cal:
		numbers = cal['reminders-text']
		for to in numbers:
			send(to, body)			