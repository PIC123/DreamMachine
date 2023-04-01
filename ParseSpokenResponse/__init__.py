import logging
import os
import openai
import json
import requests
from twilio.twiml.voice_response import Gather, VoiceResponse
from urllib.parse import urlparse, parse_qs
import uuid
import azure.functions as func

from azure.data.tables import (TableServiceClient, UpdateMode)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(parseResp(req.get_body()))
    spoken_response = parseResp(req.get_body())
    logging.info(spoken_response)

    url = "https://dream-machine-helper.azurewebsites.net/api/process"

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        'Content-Type': 'application/json',
    }
 
    data = {
        "spoken_response": spoken_response
    }

    response = requests.post(url, headers=headers, json=data)

    response = VoiceResponse()
    response.say("Thanks for sharing your dream!",voice='alice')
    return str(response)

def parseResp(resp_body):
    return [i.split('=')[1].replace('+',' ').replace('%27','\'').replace('%2C',',') for i in resp_body.decode('UTF-8').split('&') if i.split('=')[0]=='SpeechResult'][0]