from twilio.rest import Client

import project.dash_config as dc
account_sid = dc.TWILIO['account-sid']
auth_token = dc.TWILIO['auth-token']
phone_number = dc.TWILIO['phone-number']

def send(to, body):
	client = Client(account_sid, auth_token)
	message = client.messages.create(body=body, from_=phone_number, to=to)


