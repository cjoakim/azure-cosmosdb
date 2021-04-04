"""
Usage:
    python main.py load_container <db> <container> <infile> <start_idx> <count>
    python main.py load_container dev postalcodes1 data/postal_codes_us_filtered.csv 1000 99999
    python main.py load_container dev postalcodes2 data/postal_codes_us_filtered.csv 1000 99999
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.04.04"

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

def load_container(dbname, cname, infile, start_idx, count):
    c = initialize_cosmos()
    dbproxy = c.set_db(dbname)
    ctrproxy = c.set_container(cname)
    loaded_count = 0

    it = text_file_iterator(infile)
    for i, line in enumerate(it):
        if i < 1:
            pass  # skip the header line
        else:
            # 41842,99850,US,Juneau,AK,58.3016000000,-134.4194000000
            tokens = line.split(',')
            
            if i >= start_idx:
                if loaded_count < count:
                    if len(tokens) == 7:
                        try:
                            print(tokens)
                            # ['41855', '99950', 'US', 'Ketchikan', 'AK', '55.8158570000', '-132.9798500000']
                            postal_cd = tokens[1].strip()
                            state_abbrv = tokens[4].strip()
                            doc = dict()
                            doc['pk'] = state_abbrv
                            doc['original_id'] = int(tokens[0].strip())
                            doc['postal_cd'] = postal_cd
                            doc['country_cd'] = tokens[2].strip()
                            doc['city_name'] = tokens[3].strip()
                            doc['state_abbrv'] = state_abbrv
                            doc['latitude'] = float(tokens[5].strip())
                            doc['longitude'] = float(tokens[6].strip())
                            doc['epoch'] = int(time.time())
                            print(json.dumps(doc, sort_keys=False, indent=2))

                            if True:
                                result = c.upsert_doc(doc)
                                loaded_count = loaded_count + 1
                                print(result)
                                c.print_last_request_charge()
                        except:
                            pass

def text_file_iterator(infile):
    with open(infile, 'rt') as f:
        for line in f:
            yield line.strip()

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

        if func == 'load_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            infile = sys.argv[4]
            start_idx = int(sys.argv[5])
            count     = int(sys.argv[6])
            load_container(dbname, cname, infile, start_idx, count)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
