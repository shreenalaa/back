from twilio.rest import Client
from app import app

# Initialize Twilio client
client = Client('your_account_sid', 'your_auth_token')



# Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_number = 'your_twilio_phone_number'

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_sms(recipient_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=recipient_number
        )
        print(f"SMS sent successfully. SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False
