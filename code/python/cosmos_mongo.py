"""
Usage:
    python cosmos_mongo.py load_airports_by_country 
    python cosmos_mongo.py point_read dev countries aruba 945d19ba-9ea0-4f12-a4d7-e0b864338a8a 10
    python cosmos_mongo.py point_read dev countries united_states d3a493ac-4673-4279-ae64-838e4a36d245 10
    python cosmos_mongo.py gather_points_for_reading dev countries
    python cosmos_mongo.py read_points dev countries data/cosmos_mongo_points.json
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.03.04"

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
    dbname, collname = 'dev', 'countries'

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

def point_read(dbname, collname, pk, id, count):
    conn_str = os.environ['AZURE_COSMOSDB_MONGODB_CONN_STRING']
    print('conn_str: {}'.format(conn_str))

    client = MongoClient(conn_str)
    print('client: {}'.format(client))

    db = client[dbname]
    print('db: {}'.format(db))

    coll = db[collname]
    print('coll: {}'.format(coll))

    criteria = dict()
    criteria['pk'] = pk
    criteria['id'] = id

    for n in range(0, count):
        query_start_epoch = time.time()
        result = coll.find_one(criteria)
        id = result['id']
        query_end_epoch = time.time()
        elapsed_ms = (query_end_epoch - query_start_epoch) * 1000.0
        if n == 0:
            print('result document:')
            print(json.dumps(result, sort_keys=False, indent=2))
            print('criteria: {}'.format(criteria))
        print('elapsed_ms: {}  id: {}'.format(elapsed_ms, id))

def gather_points_for_reading(dbname, collname):
    conn_str = os.environ['AZURE_COSMOSDB_MONGODB_CONN_STRING']
    client = MongoClient(conn_str)
    db = client[dbname]
    coll = db[collname]
    results = list()
    cursor = coll.find( { 'size': { '$gte': 1 } }, { 'pk': 1, 'size': 1, '_id': 1, 'id': 1 } )
    for result in cursor:
        print(result)
        results.append(result)
    write_obj_as_json_file('data/cosmos_mongo_points.json', results)

def read_points(dbname, collname, infile):
    conn_str = os.environ['AZURE_COSMOSDB_MONGODB_CONN_STRING']
    client = MongoClient(conn_str)
    db = client[dbname]
    coll = db[collname]

    points_to_read = read_json(infile)
    for idx, point in enumerate(points_to_read):
        criteria = dict()
        criteria['pk'] = point['pk']
        criteria['id'] = point['id']

        query_start_epoch = time.time()
        result = coll.find_one(criteria)
        country = result['country']
        query_end_epoch = time.time()
        elapsed_ms = (query_end_epoch - query_start_epoch) * 1000.0
        #country = result['country']
        size = len(json.dumps(result))
        if idx == 0:
            print('result document:')
            print(json.dumps(result, sort_keys=False, indent=2))
        print('elapsed_ms: {}  country: {}  size: {}'.format(
            elapsed_ms, country, size))

def amtrak_stations_as_list(stations_hash):
    items = list()
    keys = sorted(stations_hash.keys())
    for key in keys:
        items.append(stations_hash[key])
    return items

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def write_obj_as_json_file(outfile, obj):
    txt = json.dumps(obj, sort_keys=True, indent=2)
    with open(outfile, 'wt') as f:
        f.write(txt)
    print("file written: " + outfile)

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
        elif func == 'point_read':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            pk = sys.argv[4]
            id = sys.argv[5]
            count = int(sys.argv[6])
            point_read(dbname, cname, pk, id, count)
        elif func == 'gather_points_for_reading':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            gather_points_for_reading(dbname, cname)
        elif func == 'read_points':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            infile = sys.argv[4]
            read_points(dbname, cname, infile)
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no command-line args entered')
