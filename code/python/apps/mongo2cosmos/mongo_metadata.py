"""
Point this utility at the "source" database to be migrated, to obtain
the list of its collections.

From this list we can easily generate code such as shell scripts to produce
mongoexport files, and to transform those mongoexport files into the
format required in the "target" Cosmos/Mongo database.

Usage:
    python mongo_metadata.py read_db_metadata <conn-str-env-var> <db-name>
    python mongo_metadata.py read_db_metadata MONGODB_LOCAL_CONN_STR migrate
    python mongo_metadata.py read_db_metadata AZURE_COSMOSDB_MONGODB_CONN_STRING dev
    python mongo_metadata.py generate_scripts <db-name>
    python mongo_metadata.py generate_scripts migrate
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.03.02"

import json
import os
import pprint
import sys
import time
import uuid

import arrow
import jinja2

from docopt import docopt

from pymongo import MongoClient

# Top-Level CLI-invoked methods below

def read_db_metadata(conn_str_env_var, dbname):
    print('dbname:           {}'.format(dbname))
    print('conn_str_env_var: {}'.format(conn_str_env_var))
    conn_str = os.environ[conn_str_env_var]
    print('conn_str:         {}'.format(conn_str))

    client = MongoClient(conn_str)
    print('client: {}'.format(client))

    db = client[dbname]
    print('db: {}'.format(db))

    coll_names = db.list_collection_names()  # api for newer versions of mongo
    #coll_names = db.collection_names()        # deprecated in version 3.7.0

    metadata = dict()
    metadata['dbname']  = dbname
    metadata['env_var'] = conn_str_env_var
    metadata['collections'] = list() 

    for coll_name in coll_names:
        coll_obj = db[coll_name]
        coll_info = dict()
        coll_info['name'] = coll_name 
        coll_info['count'] = coll_obj.count_documents({})
        coll_info['indexes'] = list()
        for index in coll_obj.list_indexes():
            coll_info['indexes'].append(index)
        metadata['collections'].append(coll_info)

    jstr = json.dumps(metadata, sort_keys=False, indent=2)
    print(jstr)
    outfile = 'data/meta/{}_metadata.json'.format(dbname)
    write(outfile, jstr)

def generate_scripts(dbname):
    print('generate_scripts, dbname: {}'.format(dbname))
    infile = 'data/meta/{}_metadata.json'.format(dbname)
    metadata = read_json(infile)
    metadata['gen_timestamp'] = arrow.utcnow().to('US/Eastern').format('YYYY-MM-DD HH:mm:ss ')

    t = get_template(os.getcwd(), 'mongoexport_script.sh')
    s = t.render(metadata)
    outfile = 'generated/{}_db_mongoexport.sh'.format(dbname)
    write(outfile, s)

    t = get_template(os.getcwd(), 'transform_script.sh')
    s = t.render(metadata)
    outfile = 'generated/{}_db_transform.sh'.format(dbname)
    write(outfile, s)

def get_template(root_dir, name):
    filename = 'templates/{}'.format(name)
    return get_jinja2_env(root_dir).get_template(filename)

def render(template, values):
    return template.render(values)

def get_jinja2_env(root_dir):
    return jinja2.Environment(
        loader = jinja2.FileSystemLoader(
            root_dir), autoescape=True)

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def write(outfile, s, verbose=True):
    with open(outfile, 'w') as f:
        f.write(s)
        if verbose:
            print('file written: {}'.format(outfile))

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        if func == 'read_db_metadata':
            conn_str_env_var = sys.argv[2]
            dbname = sys.argv[3]
            read_db_metadata(conn_str_env_var, dbname)
        elif func == 'generate_scripts':
            dbname = sys.argv[2]
            generate_scripts(dbname)
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
