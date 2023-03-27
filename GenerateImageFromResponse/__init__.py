import logging
import os
import openai
import json
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

    chat_resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant that helps fix transcription issues from phone recordings. You take in the transcription attempt and try and understand what the original message was supposed to be and reproduce it as best as you can. Include the main key words and sentiment of the statements as lists. Also include in the response json a Dall-E prompt that would turn the corrected response into an abstract digital painting with miyazaki dreamlike style and a surrealistic twist with bright colors and a lot of details. Return the response as a JSON object and only responds with the JSON. Limit the response to only the json object."},
                {"role": "user", "content": spoken_response}
            ]
    )

    fixed_message = chat_resp.get("choices")[0].get("message").get("content")
    logging.info(fixed_message)

    # prompt = fixed_message + "as an abstract digital painting with miyazaki dreamlike style and a surrealistic twist with bright colors and a lot of details"
    # img_resp = openai.Image.create(
    #     prompt=prompt,
    #     n=4,
    #     size="256x256"
    # )

    # img_urls = [x.get("url") for x in img_resp.get("data")]

    # logging.info(img_urls)
        
    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    dream_table_client = table_service_client.get_table_client(table_name="Dreams")
    dream_data = {
                "PartitionKey": "sample-anonymous-dream",
                "RowKey": str(uuid.uuid4()),
                "OriginalTranscript": spoken_response,
                "FixedTranscript": fixed_message
                # "ImageURLs": json.dumps(img_urls)
            }
    dream_table_client.create_entity(entity=dream_data)

    response = VoiceResponse()
    response.say("Thanks for sharing your dream!",voice='alice')
    return str(response)


def parseResp(resp_body):
    return [i.split('=')[1].replace('+',' ').replace('%27','\'').replace('%2C',',') for i in resp_body.decode('UTF-8').split('&') if i.split('=')[0]=='SpeechResult'][0]