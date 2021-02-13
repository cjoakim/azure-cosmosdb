"""
Usage:
    python wrangle_imdb.py tsv_to_json ../../data/imdb/name.basics.mini.tsv
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.02.13"

import json
import os
import pprint
import sys
import time
import uuid

from docopt import docopt
from os.path import abspath

def tsv_to_json(infile):
    outfile = abspath('{}.json'.format(infile))
    print('tsv_to_json: {} -> {}'.format(infile, outfile))
    start_time = time.time()
    col_names = []
    it = text_file_iterator(infile)

    with open(outfile, 'wt') as out:
        for i, line in enumerate(it):
            if i == 0:
                col_names = line.split("\t")
            else:
                col_values = line.split("\t")
                d = dict()
                d['seq'] = i
                for col_idx, col_val in enumerate(col_values):
                    col_name = col_names[col_idx]
                    d[col_name] = col_val
                out.write(json.dumps(d))
                out.write("\n")

    end_time = time.time()
    print('elapsed: {}'.format(end_time - start_time))
    print('infile:  {}'.format(infile))
    print(i)
    print(col_names)

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

        if func == 'tsv_to_json':
            infile = sys.argv[2]
            tsv_to_json(infile)

        elif func == 'xxx':
            tsv_to_json()

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
