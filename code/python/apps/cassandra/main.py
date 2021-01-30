"""
Usage:
  python main.py create_airports_table
  python main.py load_airports_table
  python main.py query_all
  python main.py query_by_code CLT
  python main.py query_ad_hoc
"""

import csv
import datetime
import json
import os
import ssl
import sys
import time
import traceback

import cassandra
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import BatchStatement, SimpleStatement
from cassandra.cluster import Cluster
from cassandra.policies import *

from docopt import docopt

from requests.utils import DEFAULT_CA_BUNDLE_PATH

from prettytable import PrettyTable

from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.11.24"


cluster, session = None, None

def connect(verbose=False):
    global cluster, session
    username = os.environ.get('AZURE_COSMOSDB_CASSANDRA_USER')
    password = os.environ.get('AZURE_COSMOSDB_CASSANDRA_PASS')
    contact_point = os.environ.get('AZURE_COSMOSDB_CASSANDRA_URI')
    port = os.environ.get('AZURE_COSMOSDB_CASSANDRA_PORT')

    if verbose:
        print('cassandra_config:')
        print('  username:      {}'.format(username))
        print('  password:      {}'.format(password))
        print('  contact_point: {}'.format(contact_point))
        print('  port:          {}'.format(port))

    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.verify_mode = CERT_NONE

    auth_provider = PlainTextAuthProvider(
        username=username, 
        password=password)

    cluster = Cluster(
        [contact_point],
        port,
        auth_provider=auth_provider,
        ssl_context=ssl_context)
    if verbose:
        print('cluster: {}'.format(cluster))

    session = cluster.connect()
    if verbose:
        print('session: {}'.format(session))

def close():
    if cluster != None:
        print('closing cluster...')
        cluster.shutdown()
        print('cluster closed')
    else:
        print('close - cluster is None')

def create_airports_table():
    print('create_airports_table')
    keyspace_name = 'travel'
    drop_ks_ddl   = drop_keyspace_ddl(keyspace_name)
    create_ks_ddl = create_keyspace_ddl(keyspace_name)
    create_tbl_ddl = airports_table_ddl()

    connect(True)

    print('executing: {}'.format(drop_ks_ddl))
    rs = session.execute(drop_ks_ddl)  # <cassandra.cluster.ResultSet object at 0x1024779a0>
    for r in rs:
        print(r)

    print('executing: {}'.format(create_ks_ddl))
    rs = session.execute(create_ks_ddl)
    for r in rs:
        print(r)

    print('executing: {}'.format(create_tbl_ddl))
    rs = session.execute(create_tbl_ddl) 
    for r in rs:
        print(r)

    close()

def drop_keyspace_ddl(name):
    return 'DROP KEYSPACE IF EXISTS {};'.format(name)

def create_keyspace_ddl(name):
    s = "CREATE KEYSPACE IF NOT EXISTS {} WITH replication = <'class': 'NetworkTopologyStrategy', 'datacenter' : '1' >;".format(name)
    return s.replace('<','{').replace('>','}')

def airports_table_ddl():
    return """
CREATE TABLE travel.airports(
  "code"       text,
  "name"       text,
  "city"       text,
  "country"    text,
  "tz_name"    text,
  "tz_num"     int,
  "lat"        double,
  "lon"        double,
  "alt"        int,
  PRIMARY KEY (code)
);
""".strip()

def airports_table_ddl_orig():
    return """
CREATE TABLE travel.airports(
  "code"       text,
  "name"       text,
  "city"       text,
  "country"    text,
  "tz_name"    text,
  "tz_num"     int,
  "lat"        double,
  "lon"        double,
  "alt"        int,
  PRIMARY KEY (code)
);
""".strip()

def load_airports_table():
    print('load_airports_table')
    template_parts = list()
    template_parts.append('INSERT INTO travel.airports ')
    template_parts.append('(code,name,city,country,tz_name,tz_num,lat,lon,alt) ')
    template_parts.append('VALUES (')
    template_parts.append("'{}',",)
    template_parts.append("'{}',",)
    template_parts.append("'{}',",)
    template_parts.append("'{}',",)
    template_parts.append("'{}',",)
    template_parts.append("{},",)
    template_parts.append("{},",)
    template_parts.append("{},",)
    template_parts.append("{}",)
    template_parts.append(')')
    template = "".join(template_parts)
    print(template)

    #      0          1       2         3          4           5           6            7           8            9          10      11                                 
    # ['AirportId', 'Name', 'City', 'Country', 'IataCode', 'IcaoCode', 'Latitude', 'Longitude', 'Altitude', 'TimezoneNum', 'Dst', 'TimezoneCode']
    # ['3876', 'Charlotte Douglas Intl', 'Charlotte', 'United States', 'CLT', 'KCLT', '35.214', '-80.943139', '748', '-5', 'A', 'America/New_York']
    rows = read_csv('data/openflights_airports.csv', skip=1)
    statements = list()

    for row in rows:
        try:
            code = row[4].replace("'","").upper()
            name = row[1].replace("'","")
            city = row[2].replace("'","")
            country = row[3].replace("'","")
            tz_name = row[11]
            tz_num  = int(row[9])
            lat  = float(row[6])
            lon  = float(row[7])
            alt  = int(row[8])

            if len(code.strip()) > 2:
                stmt = template.format(code,name,city,country,tz_name,tz_num,lat,lon,alt)
                statements.append(stmt)
        except:
            traceback.print_exc()

    count = len(statements)
    print('statements count: {}'.format(count))

    if count > 0:
        connect(True)
        for stmt_idx, stmt in enumerate(statements):
            if stmt_idx < 9999:
                try:
                    print(stmt)
                    rs = session.execute(stmt) 
                    for r in rs:
                        print(r)
                except:
                    traceback.print_exc()
        close()

def query_all():
    connect(True)
    stmt = 'SELECT * FROM travel.airports'
    print(stmt)
    rs = session.execute(stmt) 
    for r in rs:
        print(r)
    close()

def query_by_code(code):
    connect(True)
    stmt = "SELECT * FROM travel.airports where code = '{}'".format(code)
    print(stmt)
    rs = session.execute(stmt) 
    for r in rs:
        print(r)
    close()

def query_ad_hoc():
    connect(True)
    stmt = "SELECT * FROM travel.airports where alt > 5000 ALLOW FILTERING"
    print(stmt)
    rs = session.execute(stmt) 
    for r in rs:
        print(r)
    close()

def print_table(rows):
    cols = 'code,name,city,country,tz_name,tz_num,lat,lon,alt'.split(',')
    t = PrettyTable(cols)
    for r in rows:
        t.add_row([r.code, r.name, r.city, r.country, r.tz_name. r.tz_num, r.lat, r.lon, r.alt])
    print(t)

def read_text(infile):
    with open(infile, 'rt') as f:
        return f.read()

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def read_lines(infile):
    lines = list()
    with open(infile, 'rt') as f:
        for line in f:
            lines.append(line)
    return lines

def read_csv(infile, reader='default', delim=',', dialect='excel', skip=0):
    rows = list()
    if reader == 'dict':
        with open(infile, 'rt') as csvfile:
            rdr = csv.DictReader(csvfile, dialect=dialect, delimiter=delim)
            for row in rdr:
                rows.append(row)
    else:
        with open(infile) as csvfile:
            rdr = csv.reader(csvfile, delimiter=delim)
            for idx, row in enumerate(rdr):
                if idx >= skip:
                    rows.append(row)
    return rows

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        if func == 'create_airports_table':
            create_airports_table()
        elif func == 'load_airports_table':
            load_airports_table()
        elif func == 'query_all':
            query_all()
        elif func == 'query_by_code':
            code = sys.argv[2].upper()
            query_by_code(code)
        elif func == 'query_ad_hoc':
            query_ad_hoc()
        else:
            print_options('invalid command line function: {}'.format(func))    
    else:
        print_options('no command-line args given')
