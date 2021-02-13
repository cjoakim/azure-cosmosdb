"""
Usage:
    python wrangle_imdb.py tsv_to_json ../../data/imdb/name.basics.mini.tsv
    python wrangle_imdb.py tsv_to_mongoexport ../../data/imdb/name.basics.mini.tsv
    python wrangle_imdb.py tsv_to_mongoexport ../../data/imdb/name.basics.tsv
    python wrangle_imdb.py transform_mongoexport_file ../../data/imdb/name.basics.mini.tsv.mongoexport.json
    python wrangle_imdb.py transform_mongoexport_file ../../data/imdb/name.basics.tsv.mongoexport.json
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
from bson.objectid import ObjectId

def tsv_to_json(infile):
    # create a "json document per line" output file from the input tsv file
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

def tsv_to_mongoexport(infile):
    # synthesize an outfile in "mongoexport" format from the input tsv file
    outfile = abspath('{}.mongoexport.json'.format(infile))
    print('tsv_to_mongoexport: {} -> {}'.format(infile, outfile))
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
                # See https://pymongo.readthedocs.io/en/stable/api/bson/objectid.html
                d['_id'] = str(ObjectId())  # bson.objectid.ObjectId
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

    # Results; 10.7 million rows/documents in 138 seconds
    # elapsed: 138.10370182991028
    # infile:  ../../data/imdb/name.basics.tsv
    # 10713449

def transform_mongoexport_file(infile):
    # "wrangle" (i.e. - transform) the values in the input mongoexport file to a similar output mongoexport file
    outfile = abspath('transformed.mongoexport.json'.format(infile))
    print('transform_mongoexport_file: {} -> {}'.format(infile, outfile))
    start_time = time.time()
    it = text_file_iterator(infile)

    with open(outfile, 'wt') as out:
        for i, line in enumerate(it):
            doc = json.loads(line)
            if i < 3:
                print(json.dumps(doc, sort_keys=True, indent=2))
                # Sample input (pretty) JSON doc
                # {
                #   "_id": "60281df10f3e7502b8a7a316",
                #   "birthYear": "1899",
                #   "deathYear": "1987",
                #   "knownForTitles": "tt0050419,tt0053137,tt0031983,tt0072308",
                #   "nconst": "nm0000001",
                #   "primaryName": "Fred Astaire",
                #   "primaryProfession": "soundtrack,actor,miscellaneous",
                #   "seq": 1
                # }

            # Reformatting logic; delete the _id, add pk, convert two attributes to arrays
            del doc['_id']  # a new ObjectId will be generated in the target database
            doc['pk'] = doc['birthYear']  # birthYear is used here as an example partition key, not necessarily recommended
            doc['primaryProfession'] = doc['primaryProfession'].split(',')  # convert string to array
            doc['knownForTitles'] = doc['knownForTitles'].split(',')  # convert string to array

            if i < 3:
                print(json.dumps(doc, sort_keys=True, indent=2))
                # Sample reformatted (pretty) JSON doc
                # {
                #   "birthYear": "1899",
                #   "deathYear": "1987",
                #   "knownForTitles": [
                #     "tt0050419",
                #     "tt0053137",
                #     "tt0031983",
                #     "tt0072308"
                #   ],
                #   "nconst": "nm0000001",
                #   "pk": "1899",
                #   "primaryName": "Fred Astaire",
                #   "primaryProfession": [
                #     "soundtrack",
                #     "actor",
                #     "miscellaneous"
                #   ],
                #   "seq": 1
                # }

            out.write(json.dumps(doc))
            out.write("\n")

    end_time = time.time()
    print('elapsed: {}'.format(end_time - start_time))
    print('infile:  {}'.format(infile))
    print(i)

    # Results; 10.7 million rows/documents in 143 seconds
    # elapsed: 142.51749515533447
    # infile:  ../../data/imdb/name.basics.tsv.mongoexport.json
    # 10713448

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

        elif func == 'tsv_to_mongoexport':
            infile = sys.argv[2]
            tsv_to_mongoexport(infile)

        elif func == 'transform_mongoexport_file':
            infile = sys.argv[2]
            transform_mongoexport_file(infile)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
