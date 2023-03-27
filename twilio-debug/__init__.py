import logging
from twilio.twiml.voice_response import Gather, VoiceResponse

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:

    response = VoiceResponse()
    response.say('Chapeau!', voice='woman', language='fr-FR')

    print(response)
    return str(response)
    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
