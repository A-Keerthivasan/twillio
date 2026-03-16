import keys
from twilio.rest import Client
import sys

# Twilio client setup
account_sid = keys.account_sid
account_token = keys.auth_token
client = Client(account_sid, account_token)

# Get recipient argument (default to 'Public' if not provided)
recipient = sys.argv[1] if len(sys.argv) > 1 else 'Public'

# Define messages for each recipient
if recipient == 'Corporation':
    alert_message = '🚨 AquaAssistant Alert: Water leakage detected in your area! Please take necessary action. 💧'
    call_message = 'AquaAssistant Alert: Water leakage detected in your area! Please take necessary action. Have a great day!'
elif recipient == 'DWLR Service Manager':
    alert_message = '🚨 AquaAssistant Alert: DWLR unit malfunction detected. Immediate service required! 💧'
    call_message = 'AquaAssistant Alert: DWLR unit malfunction detected. Immediate service required. Have a great day!'
elif recipient == 'Farmer':
    alert_message = '🚨 AquaAssistant Alert: Ground water level is critically low in your region! Consider water conservation measures for irrigation. 💧'
    call_message = 'AquaAssistant Alert: Ground water level is critically low in your region. Please optimize irrigation and consider water conservation practices. Have a great day!'
else:
    alert_message = '🚨 AquaAssistant Alert: Your water level is very low! Please take immediate action. 💧'
    call_message = 'AquaAssistant Alert: Your water level is very low or the system is under maintenance. Please check. Have a great day!'

# Send SMS
message = client.messages.create(
    from_=keys.twilio_number,
    body=alert_message,
    to=keys.my_phone_number
)
print(f"Message sent to {recipient} with SID: {message.sid}")

# Make a voice call
call = client.calls.create(
    from_=keys.twilio_number,
    to=keys.my_phone_number,
    twiml=f'<Response><Say>{call_message}</Say></Response>'
)
print(f"Call initiated to {recipient} with SID: {call.sid}")
