
import json
import logging
import os
import string
import time 

import azure.functions as func

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import azure.cosmos.diagnostics as diagnostics
import azure.cosmos.documents as documents
import azure.cosmos.exceptions as exceptions
import azure.cosmos.partition_key as partition_key

FUNCTION_VERSION = '2020/10/10 13:44'

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        start_time = time.time()
        logging.error('request received at epoch time: {}  version'.format(
            start_time, FUNCTION_VERSION))
        body = req.get_json()  # this is already a dict object, not a string
        # logging.error(body)
        logging.error(str(type(body)))
        updated_at = body['updated_at']
        plants = body['plants']
        logging.error('updated_at:   {} {}'.format(updated_at, str(type(updated_at))))
        logging.error('plants count: {}'.format(len(plants)))
        #logging.error('plants: {}'.format(plants))

        url = os.environ['AZURE_COSMOSDB_SQLDB_URI']
        key = os.environ['AZURE_COSMOSDB_SQLDB_KEY']
        logging.error('cosmos url: {}'.format(url))
        logging.error('cosmos key: {}'.format(key))

        client = cosmos_client.CosmosClient(url, {'masterKey': key})
        logging.error('client: {}'.format(client))

        if body:
            results = process_request(start_time, updated_at, plants, client)
            return func.HttpResponse(results, mimetype="application/json")
        else:
            return func.HttpResponse("Null body", status_code=400)
    except:
        return func.HttpResponse("Exception", status_code=400)

def process_request(start_time, updated_at, plants, client):
    logging.warn('process_request, updated_at: {} {}'.format(updated_at, str(type(updated_at))))
    results = dict()
    results['upserts'] = list()

    plant_count = len(plants)
    logging.warn('process_request, plants length: {}'.format(plant_count))

    if plant_count > 0:
        db_client = client.get_database_client(db_name())
        logging.warn('db_client: {}'.format(db_client))
        container_client = db_client.get_container_client(container_name())
        logging.warn('container_client: {}'.format(container_client))

        for idx, plant in enumerate(plants):
            pass
            if plant['updated_at'] >= updated_at:
                logging.warn('upserting: {}'.format(plant))
                item = container_client.upsert_item(plant)
                results['upserts'].append(item)
                logging.warn('upserted: {}'.format(item))

    summary = dict()
    results['summary'] = summary
    summary['upsert_count'] = len(results['upserts'])
    summary['function_version'] = FUNCTION_VERSION
    summary['start_time'] = start_time
    summary['finish_time'] = time.time()
    summary['elapsed_time'] = summary['finish_time'] - start_time
    return json.dumps(results, ensure_ascii=False)

def db_name():
    return 'dev'     # we could reimplement this and read an environment variable

def container_name():
    return 'plants'  # we could reimplement this and read an environment variable
