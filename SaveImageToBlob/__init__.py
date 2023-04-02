import logging
from PIL import Image
import requests
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.data.tables import (TableServiceClient, UpdateMode)


import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    
    req_body = req.get_json()

    logging.info(f"req body: {req_body}")

    imgUrl = req_body.get('imgURL')

    blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONN_STRING)

    container_name = "dreams"
    file_name = f"{req_body.get('id')}.png"

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    # im = Image.open(requests.get(imgUrl, stream=True).raw)

    blob_client.upload_blob_from_url(imgUrl)

    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    state_table_client = table_service_client.get_table_client(table_name="state")
    state_data = {
                "PartitionKey": "0",
                "RowKey": "0",
                "latestImgUrl": f"https://dreammachinesa.blob.core.windows.net/dreams/{file_name}",
                "isInUse": False,
            }
    state_table_client.update_entity(entity=state_data)

    return func.HttpResponse(
                "Saved image to blob",
                status_code=200
        )