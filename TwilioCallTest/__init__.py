import logging
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # response = VoiceResponse()
    # gather = Gather(input='speech', action='/generate')

    # # Use <Say> to give the caller some instructions
    # gather.say('Hello, and welcome to Dreambox! After the tone, please record a dream you have that you want to visualize and share with the world.')
    # response.append(gather)
    response = VoiceResponse()
    gather = Gather(input='speech', action='/generated')
    gather.say('Hello, and welcome to Dreambox! After the tone, please record a dream you have that you want to visualize and share with the world.')
    response.append(gather)

    print(response)

    return str(response)
