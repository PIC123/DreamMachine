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

    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    state_table_client = table_service_client.get_table_client(table_name="state")
    state = state_table_client.list_entities().next()
    state_data = {
                "PartitionKey": "0",
                "RowKey": "0",
                "isInUse": True,
                "userCount": state.get("userCount") + 1,
            }
    state_table_client.update_entity(entity=state_data)

    logging.info(parseResp(req.get_body()))
    spoken_response = parseResp(req.get_body())
    logging.info(spoken_response)

    if(spoken_response == "The Google subscriber you've called is not available. Please leave a message after the tone."):
        return func.HttpResponse(
            "No response",
            status_code=200
        )

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

    requests.post(url, headers=headers, json=data)

    response = VoiceResponse()
    response.say("Thanks for sharing your dream!", voice='alice')
    return str(response)

def parseResp(resp_body):
    return [i.split('=')[1].replace('+',' ').replace('%27','\'').replace('%2C',',') for i in resp_body.decode('UTF-8').split('&') if i.split('=')[0]=='SpeechResult'][0]