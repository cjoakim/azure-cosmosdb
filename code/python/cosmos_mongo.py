"""
Usage:
    python cosmos_mongo.py load_cosmos_mongo /Users/cjoakim/github/cj-data/airports/us_airports.json
    python cosmos_mongo.py load_airports_by_country 
    python cosmos_mongo.py query_cosmos_mongo 
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.01.31"

import json
import os
import pprint
import sys
import time
import uuid

from docopt import docopt

from pymongo import MongoClient

from pysrc.cjcc.constants import Constants
from pysrc.cjcc.cosmos import Cosmos
from pysrc.cjcc.env import Env
from pysrc.cjcc.fs import FS
from pysrc.cjcc.mongo import Mongo

# Top-Level CLI-invoked methods below

def load_airports_by_country():
    infile = 'data/airports_by_country.json'
    countries = read_json(infile)
    dbname, collname = 'dev', 'airports'

    conn_str = os.environ['AZURE_COSMOSDB_MONGODB_CONN_STRING']
    print('conn_str: {}'.format(conn_str))

    client = MongoClient(conn_str)
    print('client: {}'.format(client))

    db = client[dbname]
    print('db: {}'.format(db))

    coll = db[collname]
    print('coll: {}'.format(coll))

    for idx, key in enumerate(sorted(countries.keys())):
        if idx < 9999:
            try:
                country = countries[key]
                country['id'] = str(uuid.uuid4())
                country['iata_code'] = key
                print(country)
                result = coll.insert_one(country)
                print('result: {}'.format(result))
                time.sleep(1)
            except:
                pass
    us = coll.find_one({'pk': 'united_states'})
    print('united_states: {}'.format(us))

def load_cosmos_mongo(infile):
    airports = read_json(infile)
    conn_str = os.environ['AZURE_COSMOSDB_MONGODB_CONN_STRING']
    dbname, collname = 'dev', 'airports'

    print('conn_str: {}'.format(conn_str))

    client = MongoClient(conn_str)
    print('client: {}'.format(client))

    db = client[dbname]
    print('db: {}'.format(db))

    coll = db[collname]
    print('coll: {}'.format(coll))

    for airport in airports:
        airport['id'] = str(uuid.uuid4())
        airport['loc'] = airport['location']
        print('airport: {}'.format(airport))
        result = coll.insert_one(airport)
        print('result: {}'.format(result))

    clt = coll.find_one({'pk': 'CLT'})
    print('CLT: {}'.format(clt))

def query_cosmos_mongo():
    conn_str = os.environ['AZURE_COSMOSDB_MONGODB_CONN_STRING']
    print('conn_str: {}'.format(conn_str))
    dbname, collname = 'dev', 'airports'

    client = MongoClient(conn_str)
    print('client: {}'.format(client))

    db = client[dbname]
    print('db: {}'.format(db))

    coll = db[collname]
    print('coll: {}'.format(coll))

    # https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html

    clt = coll.find_one({'pk': 'CLT'})
    print('CLT: {}'.format(clt))

    count = coll.count_documents({})
    print('count, all docs: {}'.format(count))  # count: 1697

    count = coll.count_documents({"city":"Atlanta"})
    print('count, city/Atlanta: {}'.format(count))  

    results = coll.find({"city":"Atlanta"})
    for idx, result in enumerate(results):
        print('idx: {}  result: {}'.format(idx, result))

    # query = {"location": {"$near": [-84.5718333, 33.35725]}}
    # results = coll.find(query)
    # for idx, result in enumerate(results):
    #     print('idx: {}  result: {}'.format(idx, result))

def amtrak_stations_as_list(stations_hash):
    items = list()
    keys = sorted(stations_hash.keys())
    for key in keys:
        items.append(stations_hash[key])
    return items

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()

        if func == 'load_cosmos_mongo':
            infile = sys.argv[2]
            load_cosmos_mongo(infile)
        elif func == 'load_airports_by_country':
            load_airports_by_country()
        elif func == 'query_cosmos_mongo':
            query_cosmos_mongo()
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
