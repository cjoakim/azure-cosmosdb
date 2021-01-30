"""
Usage:
    source ../app-config.sh
    python cosmos_sql.py load_airports dev airports
    python cosmos_sql.py load_amtrak dev amtrak
    python cosmos_sql.py truncate_container_per_criteria dev airports all
    python cosmos_sql.py truncate_container_per_criteria dev amtrak all
    python cosmos_sql.py query dev amtrak all
    python cosmos_sql.py query dev amtrak nc_amtrak_stations
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.09.25"

import json
import os
import pprint
import sys
import time
import uuid

from docopt import docopt

from pysrc.cjcc.cosmos import Cosmos
from pysrc.cjcc.env import Env

# Define Named-Queries here for ease of CLI use:
named_queries = dict()
named_queries['all'] = 'select * from c'
named_queries['nc_amtrak_stations'] = 'select * from c where c.state = "NC"'

def initialize_cosmos():
    opts = dict()
    opts['url'] = Env.var('AZURE_COSMOSDB_SQLDB_URI')
    opts['key'] = Env.var('AZURE_COSMOSDB_SQLDB_KEY')
    return Cosmos(opts)

def load_airports(dbname, cname):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)

    infile = '/Users/cjoakim/github/cj-data/airports/us_airports.json'
    items = read_json(infile)

    for idx, obj in enumerate(items):
        obj_keys = obj.keys()
        if 'id' in obj_keys:
            del obj['id']
        if idx < 10_000:
            if 'iata_code' in obj_keys:
                obj['pk'] = obj['iata_code']

            if len(obj['pk'].strip()) > 2:
                obj['epoch'] = time.time()
                print(json.dumps(obj, sort_keys=False, indent=2))
                result = c.upsert_doc(obj)
                print(result)
                c.print_last_request_charge()

def load_amtrak(dbname, cname):
    c = initialize_cosmos()
    c.set_db(dbname)
    c.set_container(cname)
    do_upsert = True

    infile = '/Users/cjoakim/github/cj-data/trains/amtrak/Amtrak_Merged_Stations_Routes.json'
    data = read_json(infile)
    stations = dict_as_list(data['stations'])
    routes   = data['routes']
    graph    = data['adjacent_stations']

    for idx, obj in enumerate(stations):
        obj_keys = obj.keys()
        if 'id' in obj_keys:
            del obj['id']
        if idx < 10_000:
            if 'station_code' in obj_keys:
                obj['pk'] = obj['station_code']
                obj['doctype'] = 'station'
                if 'lat' in obj_keys:
                    if 'lng' in obj_keys:
                        loc = dict()
                        loc['type'] = 'Point'
                        lat, lng = float(obj['lat']), float(obj['lng'])
                        loc['coordinates'] = [ lng, lat ]
                        del obj['lat']
                        del obj['lng']
                        obj['location'] = loc 
            if len(obj['pk'].strip()) > 2:
                obj['epoch'] = time.time()
                print(json.dumps(obj, sort_keys=False, indent=2))
                if do_upsert:
                    result = c.upsert_doc(obj)
                    print(result)
                    #c.print_last_request_charge()

    route_names = sorted(routes.keys())
    for idx, route_name in enumerate(route_names):
        obj = routes[route_name]
        obj['pk'] = route_name
        obj['doctype'] = 'route'
        obj['epoch'] = time.time()
        print(json.dumps(obj, sort_keys=False, indent=2))
        if do_upsert:
            result = c.upsert_doc(obj)
            print(result)

    graph_keys = sorted(graph.keys())
    for idx, graph_key in enumerate(graph_keys):
        station_codes = graph_key.split(':')
        obj = dict()
        obj['pk'] = graph_key
        obj['doctype'] = 'graph'
        obj['key'] = graph_key
        code1, code2 = station_codes[0], station_codes[1]
        obj['station_code_1'] = code1
        obj['station_name_1'] = data['stations'][code1]['station_name']
        obj['station_code_2'] = code2
        obj['station_name_2'] = data['stations'][code2]['station_name']
        obj['distance'] = graph[graph_key]
        obj['epoch'] = time.time()
        print(json.dumps(obj, sort_keys=False, indent=2))
        if do_upsert:
            result = c.upsert_doc(obj)
            print(result)

def query(dbname, cname, query_name):
    c = initialize_cosmos()
    c.set_db(dbname)
    c.set_container(cname)
    sql = named_queries[query_name]
    epoch = int(time.time())
    outfile = 'tmp/{}-{}.json'.format(query_name, epoch)
    print('{} -> {}'.format(query_name, sql))
    documents = list()
    query_results = c.query_container(cname, sql, True, 10000)
    if query_results == None:
        print('no query results')
    else:
        for doc in query_results:
            documents.append(doc)
        print('{} documents returned'.format(len(documents)))
        write_obj_as_json_file(outfile, documents)

def truncate_container_per_criteria(dbname, cname, criteria='all'):
    print('truncate_container_per_select; db: {}, container: {}, criteria: {}'.format(
        dbname, cname, criteria))
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)

    # TODO - enhance logic to implement different selection criteria.  For now, select all docs.
    selection_sql = 'select * from c'
    selected_documents = list()
    print('selection sql: {}'.format(selection_sql))

    # first collect the documents to be deleted
    query_results = c.query_container(cname, selection_sql, True, 10000)
    if query_results == None:
        print('no query results')
        return

    for doc in query_results:
        selected_documents.append(doc)

    for doc in selected_documents:
        print('deleting doc: {}'.format(doc))
        c.delete_doc(doc, doc['pk'])

def dict_as_list(d):
    items = list()
    keys = sorted(d.keys())
    for key in keys:
        items.append(d[key])
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

        if func == 'load_airports':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            load_airports(dbname, cname)

        elif func == 'load_amtrak':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            load_amtrak(dbname, cname)

        elif func == 'query':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            query_name = sys.argv[4]
            query(dbname, cname, query_name)

        elif func == 'truncate_container_per_criteria':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            crit   = sys.argv[4]
            truncate_container_per_criteria(dbname, cname, crit)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
