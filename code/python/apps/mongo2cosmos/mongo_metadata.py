"""
Point this utility at the "source" database to be migrated, to obtain
the list of its collections.

From this list we can easily generate code such as shell scripts to produce
mongoexport files, and to transform those mongoexport files into the
format required in the "target" Cosmos/Mongo database.

Usage:
    python mongo_metadata.py read_db_metadata <conn-str-env-var> <db-name>
    python mongo_metadata.py read_db_metadata AZURE_COSMOSDB_MONGODB_CONN_STRING dev
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.02.20"

import json
import os
import pprint
import sys
import time
import uuid

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
    metadata['coll_names'] = coll_names

    jstr = json.dumps(metadata, sort_keys=True, indent=2)
    print(jstr)
    outfile = 'data/mongo/{}_metadata.json'.format(dbname)
    write(outfile, jstr)

    # Output:
    # {
    #   "coll_names": [
    #     "amtrak",
    #     "airports"
    #   ],
    #   "dbname": "dev",
    #   "env_var": "AZURE_COSMOSDB_MONGODB_CONN_STRING"
    # }

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
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
