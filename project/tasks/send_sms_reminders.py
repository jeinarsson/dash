# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

##
## Load config
##

try:
    import project.dash_config as dc
except ModuleNotFoundError as e:
    import project.dash_config_default as dc


# Your Account Sid and Auth Token from twilio.com/console
account_sid = dc.TWILIO['account-sid']
auth_token = dc.TWILIO['auth-token']

client = Client(account_sid, auth_token)
message = client.messages.create(
                              body='test reminder..',
                              from_='+16502032813',
                              to='+16507042055'
                          )

print(message.sid)
