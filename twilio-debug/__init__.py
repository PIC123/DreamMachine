import logging
from twilio.twiml.voice_response import Gather, VoiceResponse

import requests

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:

    # response = VoiceResponse()
    # response.say('Chapeau!', voice='woman', language='fr-FR')

    url = "http://localhost:7071/api/test-http-func"

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        'Content-Type': 'application/json',
    }
 
    data = {
        "id": 1001,
        "name": "geek",
        "passion": "coding",
    }

    response = requests.post(url, headers=headers, json=data)
 
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())

    print(response)
    return str(response)
    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
