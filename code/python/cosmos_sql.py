"""
Usage:
    python cosmos_sql.py load_airports <db> <container> <start-index> <count> 
    python cosmos_sql.py load_airports dev airports  0 10
    python cosmos_sql.py load_airports dev airports 10 10
    -
    python cosmos_sql.py load_amtrak dev amtrak
    -
    python cosmos_sql.py create_database dev2 
    python cosmos_sql.py create_container dev2 airports 500
    python cosmos_sql.py get_container_throughput dev2 airports
    python cosmos_sql.py set_container_throughput dev2 airports 400
    -
    python cosmos_sql.py truncate_container dev airports
    python cosmos_sql.py truncate_container dev amtrak
    -
    python cosmos_sql.py named_query dev airports clt-airport
    python cosmos_sql.py named_query dev amtrak all
    python cosmos_sql.py named_query dev amtrak nc-amtrak-stations
    -
    python cosmos_sql.py point_query dev airports CLT 035094c9-59c7-4019-b66c-1a2e4cc12147
    python cosmos_sql.py point_query dev airports CLT 035094c9-59c7-4019-b66c-1a2e4cc12147 --upsert
    -
    python cosmos_sql.py geo_query dev airports <longitude> <latitude> <meters>
    python cosmos_sql.py geo_query dev airports -80.84309935569763 35.22718156801215 10000
    python cosmos_sql.py geo_query dev amtrak -80.84309935569763 35.22718156801215 10000
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.02.16"

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
named_queries['nc-amtrak-stations'] = 'select * from c where c.state = "NC"'
named_queries['clt-airport'] = "select * from c where c.pk = 'CLT'"

def initialize_cosmos():
    opts = dict()
    opts['url'] = Env.var('AZURE_COSMOSDB_SQLDB_URI')
    opts['key'] = Env.var('AZURE_COSMOSDB_SQLDB_KEY')
    return Cosmos(opts)

def load_airports(dbname, cname, start_idx, count):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)

    data_dir = os.environ['AZURE_COSMOSDB_DATA_DIR']
    infile = '{}/airports/us_airports.json'.format(data_dir)
    items = read_json(infile)
    loaded_count = 0

    for idx, obj in enumerate(items):
        obj_keys = obj.keys()
        if 'id' in obj_keys:
            del obj['id']
        if idx >= start_idx:
            if loaded_count < count:
                if 'iata_code' in obj_keys:
                    obj['pk'] = obj['iata_code']
                if len(obj['pk'].strip()) > 2:
                    loaded_count = loaded_count + 1
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

    data_dir = os.environ['AZURE_COSMOSDB_DATA_DIR']
    infile = '{}/amtrak/amtrak_merged_stations_routes.json'.format(data_dir)
    data   = read_json(infile)
    stations = dict_as_list(data['stations'])
    routes   = data['routes']
    graph    = data['adjacent_stations']

    for idx, obj in enumerate(stations):
        obj_keys = obj.keys()
        if 'id' in obj_keys:
            del obj['id']

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
                loaded_count = loaded_count + 1
                obj['epoch'] = time.time()
                print(json.dumps(obj, sort_keys=False, indent=2))
                if do_upsert:
                    result = c.upsert_doc(obj)
                    print(result)
                    c.print_last_request_charge()

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
            c.print_last_request_charge()

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
            c.print_last_request_charge()

def create_database(dbname):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    print(dbproxy)

def create_container(dbname, cname, throughput):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    print(dbproxy)
    ctrproxy = c.create_container(cname, '/pk', throughput)
    print(dbproxy)

def get_container_throughput(dbname, cname):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)
    offer = c.get_container_offer(cname)
    print(offer)
    print(json.dumps(offer.properties, sort_keys=True, indent=2))
    print(offer.offer_throughput)

def set_container_throughput(dbname, cname, throughput):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)
    offer = c.update_container_throughput(cname, throughput)
    print(offer)
    print(json.dumps(offer.properties, sort_keys=True, indent=2))
    print(offer.offer_throughput)

def named_query(dbname, cname, query_name):
    c = initialize_cosmos()
    c.set_db(dbname)
    c.set_container(cname)
    sql = named_queries[query_name]
    epoch = int(time.time())
    outfile = 'tmp/named-query-{}-{}.json'.format(query_name, epoch)
    print('{} -> {}'.format(query_name, sql))
    documents = list()
    query_results = c.query_container(cname, sql, True, 10000)
    if query_results == None:
        print('no query results')
    else:
        for doc in query_results:
            documents.append(doc)
        print('{} documents returned'.format(len(documents)))
        c.print_last_request_charge()
        write_obj_as_json_file(outfile, documents)

def point_query(dbname, cname, pk, id):
    c = initialize_cosmos()
    c.set_db(dbname)
    c.set_container(cname)
    sql = "select * from c where c.pk = '{}' and c.id = '{}'".format(pk, id)
    epoch = int(time.time())
    outfile = 'tmp/point-query-{}-{}-{}-{}-{}.json'.format(dbname, cname, pk, id, epoch)
    print(sql)
    documents = list()
    query_results = c.query_container(cname, sql, True, 3)
    if query_results == None:
        print('no query results')
    else:
        for doc in query_results:
            documents.append(doc)
        print('{} documents returned'.format(len(documents)))
        c.print_last_request_charge()
        write_obj_as_json_file(outfile, documents)

    if flag_cli_arg('--upsert'):
        for idx, doc in enumerate(documents):
            if idx < 1:
                epoch = time.time()
                outfile = 'tmp/point-query-{}-{}-{}-{}-{}-upsert.json'.format(dbname, cname, pk, id, int(epoch))
                doc['epoch'] = epoch
                result = c.upsert_doc(doc)
                c.print_last_request_charge()
                write_obj_as_json_file(outfile, result)

def geo_query(dbname, cname, lng, lat, meters):
    c = initialize_cosmos()
    c.set_db(dbname)
    c.set_container(cname)
    location = dict()
    location['type'] = 'Point'
    location['coordinates'] = [ float(lng), float(lat)]
    template = "select * from c where ST_DISTANCE(c.location, {}) < {}"
    sql = template.format(json.dumps(location), meters)
    epoch = int(time.time())
    outfile = 'tmp/geo-query-{}.json'.format(epoch)
    print(sql)
    documents = list()
    query_results = c.query_container(cname, sql, True, 1000)
    if query_results == None:
        print('no query results')
    else:
        for doc in query_results:
            documents.append(doc)
        print('{} documents returned'.format(len(documents)))
        c.print_last_request_charge()
        write_obj_as_json_file(outfile, documents)

def truncate_container(dbname, cname):
    print('truncate_container; db: {}, container: {}'.format(dbname, cname))
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
        c.print_last_request_charge()

def flag_cli_arg(flag):
    bool = False
    for arg in sys.argv:
        if arg == flag:
            bool = True
    return bool

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
            start_idx = int(sys.argv[4])
            count = int(sys.argv[5])
            load_airports(dbname, cname, start_idx, count)

        elif func == 'load_amtrak':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            load_amtrak(dbname, cname)

        elif func == 'create_database':
            dbname = sys.argv[2]
            create_database(dbname)

        elif func == 'create_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            throughput = int(sys.argv[4])
            create_container(dbname, cname, throughput)

        elif func == 'get_container_throughput':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            get_container_throughput(dbname, cname)

        elif func == 'set_container_throughput':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            throughput = int(sys.argv[4])
            set_container_throughput(dbname, cname, throughput)

        elif func == 'named_query':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            query_name = sys.argv[4]
            named_query(dbname, cname, query_name)

        elif func == 'point_query':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            pk     = sys.argv[4]
            id     = sys.argv[5]
            point_query(dbname, cname, pk, id)

        elif func == 'geo_query':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            lng    = sys.argv[4]
            lat    = sys.argv[5]
            meters = sys.argv[6]
            geo_query(dbname, cname, lng, lat, meters)

        elif func == 'truncate_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            truncate_container(dbname, cname)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
