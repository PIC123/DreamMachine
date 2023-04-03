import os
import logging

import azure.functions as func

from twilio.rest import Client


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
    TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
    DREAM_MACHINE_PHONE_NUMBER = os.environ["DREAM_MACHINE_PHONE_NUMBER"]

    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_client.calls.create(
        twiml='<Response><Gather action="https://dream-machine-helper.azurewebsites.net/api/parse" input="speech"><Say>Hello, and welcome to Dream Machine! After the tone, please share a dream you have that you want manifest.        BEEEEEEP.</Say></Gather></Response>',
        from_=TWILIO_PHONE_NUMBER,
        to=DREAM_MACHINE_PHONE_NUMBER,
    )
    return func.HttpResponse(
        "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
        status_code=200,
    )
