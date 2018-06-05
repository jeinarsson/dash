import project.utils.events as events
import project.dash_config as dc
from project.db import make_session

import sendgrid
from sendgrid.helpers.mail import *

apikey=dc.SENDGRID['api-key']

def send(to, subject, body):
	sg = sendgrid.SendGridAPIClient(apikey=apikey)
	from_email = Email("hashtagdo@jonaseinarsson.se")
	to_email = Email(to)
	content = Content("text/plain", body)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	print('sent', to, subject,'\n',body)


s = make_session()
(due, overdue) = events.get_reminders(s)


for e in due:
	item = e['summary'].replace('#do', '').strip()
	subject = 'Due now: {}'.format(item)
	body = "Sent by #do. Have a great day."
	if 'reminders-email' in e:
		for to in e['reminders-email']:
			send(to, subject, body)

for e in overdue:
	item = e['summary'].replace('#do', '').strip()
	subject = '! Overdue: {}'.format(item)
	body = "Sent by #do. Have a great day."
	if 'reminders-email' in e:
		for to in e['reminders-email']:
			send(to, subject, body)

print('done.')
