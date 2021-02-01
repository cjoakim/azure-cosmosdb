"""
Usage:
  python main.py populate_cosmos dev events 10 true
  python main.py truncate_container dev events 10
  python main.py truncate_container dev changes 10
  python main.py pre_restore_query dev events changes Raleigh
  python main.py restore dev events changes Davidson 28035 1592926509 
  python main.py restore dev events changes Davidson 28036 1592926509 
  python main.py backup dev events Davidson

  SELECT c.id, c.epoch, c.pk FROM c where c.epoch > 1593183000
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "2020.06.26"

import json
import os
import sys
import random
import time
import traceback

import arrow

from docopt import docopt

from pysrc.cosmos import Cosmos

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)

def populate_cosmos(dbname, cname, max_count, do_upserts):
    populate, msg_count, zipcodes_array = True, 0, read_nc_zipcodes_data()

    c = Cosmos(cosmos_connection_opts())
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)

    while msg_count < max_count:
        try:
            msg_count = msg_count + 1
            doc = random_zipcode(zipcodes_array, msg_count)
            print(json.dumps(doc, sort_keys=False, indent=4))
            if do_upserts.lower() == 'true':
                result = c.upsert_doc(doc)
                c.print_last_request_charge()
                time.sleep(0.25)
        except:
            sys.stderr.write('Exception encountered')
            traceback.print_exc(file=sys.stderr)

def truncate_container(dbname, cname, max_count):
    populate, msg_count, zipcodes_array = True, 0, read_nc_zipcodes_data()
    c = Cosmos(cosmos_connection_opts())
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)

    sql = "select * from c offset 0 limit {}".format(max_count)
    print('query - db: {}, container: {}, sql: {}'.format(dbname, cname, sql))
    docs = c.query_container(cname, sql, True, max_count)
    c.print_last_request_charge()
    deleted_count = 0

    for doc in docs:
        print('deleting: {}'.format(json.dumps(doc, sort_keys=False, indent=2)))
        c.delete_doc(doc, doc['pk'])
        c.print_last_request_charge()
        deleted_count = deleted_count + 1
        time.sleep(0.25)
    print('{} documents deleted'.format(deleted_count))

def pre_restore_query(dbname, target_cname, changes_cname, city):
    c = Cosmos(cosmos_connection_opts())
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(changes_cname)
    sql = "select * from c where c.city_name = '{}' order by c._ts".format(city)
    report_lines = list()

    # Read the changes collection for candidate docs to restore
    print('query container {}; sql: {}'.format(changes_cname, sql))
    docs = c.query_container(changes_cname, sql, True, 1)
    for doc in docs:
        line = '{},{},{},{},{}'.format(
            doc['_ts'], changes_cname, doc['pk'], doc['_originalId'], doc['city_name'])
        report_lines.append(line)

    # Read the events collection for the doc to be restored
    ctrproxy = c.set_container(target_cname)
    print('query container {}; sql: {}'.format(target_cname, sql))
    docs = c.query_container(target_cname, sql, True, 1)
    for doc in docs:
        line = '{},{},{},{},{}'.format(
            doc['_ts'], target_cname, doc['pk'], doc['id'], doc['city_name'])
        report_lines.append(line)

    # print the report, sorted by _ts, collection, pk, id, city
    for line in sorted(report_lines): 
        print(line) 

def restore(dbname, target_cname, changes_cname, city, pk, as_of_epoch):
    c = Cosmos(cosmos_connection_opts())
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(changes_cname)

    # Read the first matching changes doc <= the given as_of_epoch
    sql = "select * from c where c.city_name = '{}' and c.pk = '{}' and c._ts <= {} order by c._ts offset 0 limit 1".format(city, pk, as_of_epoch)
    print('query container {}; sql: {}'.format(changes_cname, sql))
    docs = c.query_container(changes_cname, sql, True, 1)
    c.print_last_request_charge()
    last_good_changed_doc = None
    for idx, doc in enumerate(docs):
        if idx == 0:
            last_good_changed_doc = doc
            print(json.dumps(doc, sort_keys=False, indent=2))

    if last_good_changed_doc:
        ctrproxy = c.set_container(target_cname)
        last_good_changed_doc['restored_at'] = arrow.utcnow().timestamp
        last_good_changed_doc['id'] = last_good_changed_doc['_originalId']
        print('restoring doc: {}'.format(json.dumps(last_good_changed_doc, sort_keys=False, indent=2)))
        result = c.upsert_doc(last_good_changed_doc)
        print(result)
    else:
        print('no documents met the restore criteria')

def backup(dbname, cname, city):
    c = Cosmos(cosmos_connection_opts())
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)
    sql = "select * from c where c.city_name = '{}'".format(city)
    print('sql: {}'.format(sql))
    docs, array = c.query_container(cname, sql, True, 10000), list()
    for doc in docs:
        array.append(doc)
    outfile = 'tmp/backup_{}.json'.format(city).lower()
    write(outfile, json.dumps(array), verbose=True)

def adhoc():
    c = Cosmos(cosmos_connection_opts())
    dbproxy = c.set_db('dev')
    ctrproxy = c.set_container('changes')
    # select * from c where ENDSWITH(c.city_name, 'Ford', false)  # true is case insensitive
    sql = "select c.city_name from c where ENDSWITH(c.city_name, 'Ford', true)"
    print('sql: {}'.format(sql))
    docs = c.query_container('changes', sql, True, 1000)
    for doc in docs:
        print(json.dumps(doc, sort_keys=False, indent=2))

# ========== private methods follow ==========

def cosmos_connection_opts():
    opts = dict()
    opts['url'] = os.environ['AZURE_COSMOSDB_SQLDB_URI']
    opts['key'] = os.environ['AZURE_COSMOSDB_SQLDB_KEY']
    return opts

def random_zipcode(zipcodes_array, msg_count):
    idx = random.randint(0, len(zipcodes_array) - 1)
    doc = zipcodes_array[idx]
    utc = arrow.utcnow()
    doc['id'] = doc['postal_cd']
    doc['pk'] = doc['postal_cd']
    doc['seq'] = msg_count
    doc['doctype'] = 'zipcode'
    doc['timestamp'] = utc.format('YYYY-MM-DD HH:mm:s')
    doc['epoch'] = utc.timestamp
    return doc

def read_nc_zipcodes_data():
    return read_json('data/nc_zipcodes.json')

def container_link(dbname, cname):
    return 'dbs/{}/colls/{}'.format(dbname, cname)

def create_cosmos_client():
    uri = os.environ['AZURE_COSMOSDB_SQLDB_URI']
    key = os.environ['AZURE_COSMOSDB_SQLDB_KEY']
    print('creating cosmos client with uri: {}'.format(uri))
    return cosmos_client.CosmosClient(uri, {'masterKey': key})

def read_lines(infile):
    lines = list()
    with open(infile, 'rt') as f:
        for line in f:
            lines.append(line)
    return lines

def read_file(infile):
    with open(infile, 'rt') as f:
        return f.read()

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def write(outfile, s, verbose=True):
    with open(outfile, 'w') as f:
        f.write(s)
        if verbose:
            print('file written: {}'.format(outfile))


if __name__ == "__main__":
    func = None
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()

        if func == 'populate_cosmos':
            dbname, cname = sys.argv[2], sys.argv[3]
            max_count, do_upserts = int(sys.argv[4]), sys.argv[5]
            populate_cosmos(dbname, cname, max_count, do_upserts)

        elif func == 'truncate_container':
            dbname, cname, max_count = sys.argv[2], sys.argv[3], int(sys.argv[4])
            truncate_container(dbname, cname, max_count)

        elif func == 'pre_restore_query':
            dbname, target_cname, changes_cname = sys.argv[2], sys.argv[3], sys.argv[4]
            city= sys.argv[5]
            pre_restore_query(dbname, target_cname, changes_cname, city)

        elif func == 'restore':
            dbname, target_cname, changes_cname = sys.argv[2], sys.argv[3], sys.argv[4]
            city, pk, as_of_epoch = sys.argv[5], sys.argv[6], int(sys.argv[7])
            restore(dbname, target_cname, changes_cname, city, pk, as_of_epoch)

        elif func == 'backup':
            dbname, cname, city = sys.argv[2], sys.argv[3], sys.argv[4]
            backup(dbname, cname, city)

        elif func == 'adhoc':
            adhoc()
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: invalid function: {}'.format(func))
