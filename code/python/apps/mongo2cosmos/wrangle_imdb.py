"""
This Python script reads an IMDb TSV file and produces an output file in
mongoexport format, to simulate an export from a "source" database.

Usage:
    python wrangle_imdb.py tsv_to_mongoexport <infile> <outfile>
    python wrangle_imdb.py tsv_to_mongoexport data/imdb/name_basics_small.tsv data/mongo/name_basics_small_source.json
    python wrangle_imdb.py tsv_to_mongoexport data/imdb/title_basics_small.tsv data/mongo/title_basics_small_source.json
Output:

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
from os.path import abspath
from bson.objectid import ObjectId

def tsv_to_mongoexport(infile, outfile):
    print('tsv_to_mongoexport: {} -> {}'.format(infile, outfile))
    start_time = time.time()
    col_names = []
    it = text_file_iterator(infile)

    with open(outfile, 'wt') as out:
        for i, line in enumerate(it):
            if i == 0:
                col_names = line.split("\t")
                print('col_names: {}'.format(col_names))
            else:
                col_values = line.split("\t")
                d = dict()
                # See https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html
                d['_id'] = str(ObjectId())  # bson.objectid.ObjectId
                d['seq'] = i
                for col_idx, col_val in enumerate(col_values):
                    col_name = col_names[col_idx]
                    d[col_name] = col_val
                out.write(json.dumps(d))
                out.write("\n")

    print('elapsed: {}'.format(time.time() - start_time))
    print('infile:  {}'.format(infile))
    print('outfile: {}'.format(outfile))
    print(i)

    # Results; 10.7 million rows/documents in 138 seconds
    # elapsed: 138.10370182991028
    # infile:  ../../data/imdb/name.basics.tsv
    # 10713449

def text_file_iterator(infile):
    # return a line generator that can be iterated with iterate()
    with open(infile, 'rt') as f:
        for line in f:
            yield line.strip()

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        if func == 'tsv_to_mongoexport':
            infile = sys.argv[2]
            outfile = sys.argv[3]
            tsv_to_mongoexport(infile, outfile)
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
