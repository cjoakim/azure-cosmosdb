"""
Examples of using the CosmosDB REST API vs a SQL API account.

Usage:
    python cosmos_sql_rest_client.py list_databases
    python cosmos_sql_rest_client.py list_offers
    -
    python cosmos_sql_rest_client.py create_database dev 0
    python cosmos_sql_rest_client.py create_database dev3 4000

    python cosmos_sql_rest_client.py get_database dev2
    python cosmos_sql_rest_client.py list_collections dev2
    python cosmos_sql_rest_client.py get_container dev2 airports
    python cosmos_sql_rest_client.py set_container_ru dev2 airports 600
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.02.11"

# Links
# https://docs.microsoft.com/en-us/rest/api/cosmos-db/
# https://docs.microsoft.com/en-us/rest/api/cosmos-db/access-control-on-cosmosdb-resources
# https://docs.microsoft.com/en-us/azure/azure-app-configuration/rest-api-authentication-hmac

import base64
import hashlib
import hmac
import json
import os
import sys
import time
import requests
import urllib.parse

from datetime import datetime
from docopt import docopt

from request_body import RequestBody

COSMOS_REST_API_VERSION = '2018-12-31'  # '2015-12-16'


class CosmosRestClient():

    def __init__(self):
        self.cosmos_acct = os.environ['AZURE_COSMOSDB_SQLDB_ACCT'] 
        self.cosmos_key  = os.environ['AZURE_COSMOSDB_SQLDB_KEY'] 
        self.token_type  = 'master'
        self.token_version = '1.0'
        # self.u = None  # the current url
        # self.r = None  # the current requests response object

    def ad_hoc(self):
        print('ad_hoc')

    def list_databases(self):
        print('list_databases')
        verb, resource_link = 'get', ''
        headers = self.rest_headers(verb, 'dbs', resource_link)
        url = 'https://{}.documents.azure.com/dbs'.format(self.cosmos_acct)
        self.execute_http_request('list_databases', verb, url, headers)

    def list_offers(self):
        print('list_offers')
        verb, resource_link = 'get', ''
        headers = self.rest_headers(verb, 'offers', resource_link)
        url = 'https://{}.documents.azure.com/offers'.format(self.cosmos_acct)
        self.execute_http_request('list_offers', verb, url, headers)

    def create_database(self, dbname, autopilot_ru):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/create-a-database
        print('create_database: {} {}'.format(dbname, autopilot_ru))
        verb, resource_link = 'post', ''
        headers = self.rest_headers(verb, 'dbs', resource_link)
        if autopilot_ru > 0:
            settings = {"maxThroughput": autopilot_ru}
            headers['x-ms-cosmos-offer-autopilot-settings'] = json.dumps(settings)
        body = RequestBody.create_db(dbname)
        print(headers)
        print(body)
        url = 'https://{}.documents.azure.com/dbs'.format(self.cosmos_acct)
        self.execute_http_request('create_database', verb, url, headers, body)

    def get_database(self, dbname):
        print('get_database: {}'.format(dbname))
        verb, resource_link = 'get', 'dbs/{}'.format(dbname)
        headers = self.rest_headers(verb, 'dbs', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}'.format(
            self.cosmos_acct, dbname)
        self.execute_http_request('get_database', verb, url, headers)

    def list_collections(self, dbname):
        print('list_collections: {}'.format(dbname))
        verb, resource_link = 'get', 'dbs/{}'.format(dbname)
        headers = self.rest_headers(verb, 'colls', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}/colls'.format(
            self.cosmos_acct, dbname)
        self.execute_http_request('list_collections', verb, url, headers)

    def get_container(self, dbname, cname):
        print('get_container: {} {}'.format(dbname, cname))
        verb, resource_link = 'get', 'dbs/{}/colls/{}'.format(dbname, cname)
        headers = self.rest_headers(verb, 'colls', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}/colls/{}'.format(
            self.cosmos_acct, dbname, cname)
        self.execute_http_request('get_container', verb, url, headers)

    def set_container_ru(self, dbname, cname, ru):
        print('set_container_ru: {} {} {}'.format(dbname, cname, ru))
        # TODO

    def rest_headers(self, verb, resource_type, resource_link):
        rfc_7231_dt = self.rfc_7231_date()
        string_to_sign = "{}\n{}\n{}\n{}\n\n".format(
            verb, resource_type, resource_link, rfc_7231_dt).lower()
        print("string_to_sign:\n---\n{}---".format(string_to_sign))
        # string_to_sign:
        # ---
        # get
        # colls
        # dbs/dev2/colls/airports
        # tue, 09 feb 2021 19:39:00 gmt

        # ---

        decoded_secret = base64.b64decode(self.cosmos_key, validate=True)
        digest = hmac.new(decoded_secret,
            bytes(string_to_sign, 'utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode('utf-8')
        unencoded_auth = 'type={}&ver={}&sig={}'.format(
            self.token_type, self.token_version, signature)
        encoded_auth = urllib.parse.quote(unencoded_auth)

        headers = dict()
        headers['Authorization'] = encoded_auth
        headers['x-ms-version'] = COSMOS_REST_API_VERSION
        headers['x-ms-date'] = rfc_7231_dt
        return headers

    def rfc_7231_date(self):
        # Return the current timestamp in the following format:
        # Tue, 01 Nov 1994 08:12:31 GMT
        # Tue, 09 Feb 2021 15:59:00 GMT
        return datetime.utcnow().strftime('%a, %d %b %Y %H:%M:00 GMT')

    # def rfc_7231_date_with_arrow(self):
        # Return the current timestamp in the following format:
        # Tue, 01 Nov 1994 08:12:31 GMT
        # Tue, 09 Feb 2021 15:59:00 GMT
        # now   = arrow.utcnow()
        # part1 = now.format('ddd, DD MMM YYYY HH:mm:ss')
        # part2 = 'GMT'
        # return '{} {}'.format(part1, part2)

    def execute_http_request(self, function_name, method, url, headers={}, json_body={}):
        print('===')
        print("invoke: {} {} {}\nheaders: {}\nbody: {}".format(function_name, method.upper(), url, headers, json_body))
        print('---')
        if method == 'get':
            r = requests.get(url=url, headers=headers)
        elif method == 'post':
            r = requests.post(url=url, headers=headers, json=json_body)
        elif method == 'put':
            r = requests.put(url=url, headers=headers, json=json_body)
        elif method == 'delete':
            r = requests.delete(url=url, headers=headers)
        else:
            print('error; unexpected method value passed to invoke: {}'.format(method))

        print('response: {}'.format(r))
        if r.status_code < 300:
            try:
                resp_obj = json.loads(r.text)
                print(json.dumps(resp_obj, sort_keys=False, indent=2))
                print('response: {}'.format(r))
                outfile = 'tmp/{}_{}.json'.format(function_name, r.status_code)
                self.write_json_file(resp_obj, outfile)
            except Exception as e:
                print("exception processing http response".format(e))
                print(r.text)
        else:
            print(r.text)
        return r

    def load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

    def write_json_file(self, obj, outfile):
        with open(outfile, 'wt') as f:
            f.write(json.dumps(obj, sort_keys=False, indent=2))
            print('file written: {}'.format(outfile))


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        print('func: {}'.format(func))
        client = CosmosRestClient()

        if func == 'ad_hoc':
            client.ad_hoc()

        elif func == 'rfc_7231_date':
            print(client.rfc_7231_date())

        elif func == 'list_databases':
            client.list_databases()

        elif func == 'list_offers':
            client.list_offers()

        elif func == 'create_database':
            dbname = sys.argv[2]
            autopilot_ru = int(sys.argv[3])
            client.create_database(dbname, autopilot_ru)

        elif func == 'get_database':
            dbname = sys.argv[2]
            client.get_database(dbname)

        elif func == 'list_collections':
            dbname = sys.argv[2]
            client.list_collections(dbname)

        elif func == 'get_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            client.get_container(dbname, cname)

        elif func == 'set_container_ru':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            ru     = int(sys.argv[4])
            client.set_container_ru(dbname, cname, ru)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
