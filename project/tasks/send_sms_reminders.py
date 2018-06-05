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
	print('sent', to, body)


s = make_session()
(due, overdue) = events.get_reminders(s)


for e in due:
	body = "" + e['summary'].replace('#do', '').strip()
	body=body[0:160]
	if 'reminders-text' in e:
		for to in e['reminders-text']:
			send(to, body)

for e in overdue:
	body = "! " + e['summary'].replace('#do', '').strip()
	body=body[0:160]
	if 'reminders-text' in e:
		for to in e['reminders-text']:
			send(to, body)
