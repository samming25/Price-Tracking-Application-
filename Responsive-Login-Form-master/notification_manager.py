from twilio.rest import Client


TWILIO_SID = "AC

TWILIO_AUTH_TOKEN = "2

TWILIO_VIRTUAL_NUMBER = "

TWILIO_VERIFIED_NUMBER = 


class NotificationManager:

    def __init__(self, phone):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        global TWILIO_VERIFIED_NUMBER
        # TWILIO_VERIFIED_NUMBER = f'+91{phone}'

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)
