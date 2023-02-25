from twilio.rest import Client


TWILIO_SID = "ACf98c23d3ca2d5bbfb0c5f4f9dcea6630"

TWILIO_AUTH_TOKEN = "2a32ac65eaeff70754f409eeca16a78c"

TWILIO_VIRTUAL_NUMBER = "+14632326668"

TWILIO_VERIFIED_NUMBER = "+917205733967"


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
