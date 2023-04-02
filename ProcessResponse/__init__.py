import json
import logging
import os
import uuid

import azure.functions as func
import openai
from azure.data.tables import (TableServiceClient, UpdateMode)
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    spoken_response = req_body.get('spoken_response')

    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat_resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant that helps fix transcription issues from phone recordings and return JSON objects with the resulting information. You take in the transcription attempt and try and understand what the original message was supposed to be and reproduce it as best as you can, storing it under the \"corrected_message\" parameter. Include the main key words and sentiment of the statements as lists under the parameters \"keywords\", \"sentiment\" accordingly. Also include in the response json a Dall-E prompt that would turn the corrected response into an abstract digital painting with miyazaki dreamlike style and a surrealistic twist with bright colors and a lot of details and store the resulting prompt under the parameter \"dalle_prompt\". Also include the original message in the JSON object response with the property \"original_message\". Limit the response to only the json object."},
                {"role": "user", "content": spoken_response}
            ]
    )

    chat_resp = chat_resp.get("choices")[0].get("message").get("content")
    logging.info(chat_resp)

    fixed_message = json.loads(chat_resp).get("corrected_message")
    dalle_prompt = json.loads(chat_resp).get("dalle_prompt")
    keywords = json.loads(chat_resp).get("keywords")
    sentiment = json.loads(chat_resp).get("sentiment")


    img_resp = openai.Image.create(
        prompt=dalle_prompt,
        n=1,
        size="512x512"
    )

    img_urls = [x.get("url") for x in img_resp.get("data")]

    logging.info(img_urls)
        
    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    dream_table_client = table_service_client.get_table_client(table_name="Dreams")
    dream_data = {
                "PartitionKey": "sample-anonymous-dream",
                "RowKey": str(uuid.uuid4()),
                "OriginalTranscript": spoken_response,
                "FixedTranscript": fixed_message,
                "Keywords": json.dumps(keywords),
                "Sentiment": json.dumps(sentiment),
                "ImageURLs": json.dumps(img_urls),
                "DallePrompt": dalle_prompt,
            }
    dream_table_client.create_entity(entity=dream_data)

    url = "https://dream-machine-helper.azurewebsites.net/api/saveImage"

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        'Content-Type': 'application/json',
    }

    state_table_client = table_service_client.get_table_client(table_name="state")
    state = state_table_client.list_entities().next()

    data = {
        "imgURL": img_urls[0],
        "id": state.get("userCount")
    }

    logging.info(data)

    requests.post(url, headers=headers, json=data)

    return func.HttpResponse(
             json.dumps(dream_data),
             status_code=200
        )