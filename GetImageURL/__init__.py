import json
import logging
import os

import azure.functions as func

from azure.data.tables import (TableServiceClient, UpdateMode)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    STORAGE_CONN_STRING = os.environ["STORAGE_CONN_STRING"]
    table_service_client = TableServiceClient.from_connection_string(conn_str=STORAGE_CONN_STRING)
    state_table_client = table_service_client.get_table_client(table_name="state")
    state = state_table_client.list_entities().next()
    latestImgURL = state.get("latestImgUrl")
    resp_data = {
        "url": latestImgURL,
    }
    
    return func.HttpResponse(
            json.dumps(resp_data),
            status_code=200
    )
