"""
Examples of using the CosmosDB REST API vs a SQL API account.

Usage:
    - Databases:
    python cosmos_sql_rest_client.py list_databases
    python cosmos_sql_rest_client.py create_database dev 0
    python cosmos_sql_rest_client.py create_database dev2 4000
    python cosmos_sql_rest_client.py delete_database dev2
    python cosmos_sql_rest_client.py get_database dev2
    - Collections/Containers:
    python cosmos_sql_rest_client.py list_collections dev
    python cosmos_sql_rest_client.py create_container dev airports 500 /pk
    python cosmos_sql_rest_client.py get_container dev airports
    python cosmos_sql_rest_client.py delete_container dev airports 
    python cosmos_sql_rest_client.py get_pk_ranges dev airports
    - Offers/Throughput:
    python cosmos_sql_rest_client.py list_offers
    python cosmos_sql_rest_client.py get_offer 8jId
    python cosmos_sql_rest_client.py associate_offers dev
    python cosmos_sql_rest_client.py set_database_autopilot_ru dev2 5000
    python cosmos_sql_rest_client.py set_container_ru dev airports 600
    -
    python cosmos_sql_rest_client.py get_document dev airports SFO 895014e0-1d52-40f6-8ae2-f9dcb0119961
    python cosmos_sql_rest_client.py get_document dev airports PDT f9331886-a503-4fa7-b585-a134b24a5cdd
    -
    python cosmos_sql_rest_client.py help
    -
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.02.22"

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
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/list-databases
        print('list_databases')
        verb, resource_link = 'get', ''
        headers = self.__rest_headers(verb, 'dbs', resource_link)
        url = 'https://{}.documents.azure.com/dbs'.format(self.cosmos_acct)
        return self.__execute_http_request('list_databases', verb, url, headers)

    def create_database(self, dbname, autopilot_ru):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/create-a-database
        print('create_database: {} {}'.format(dbname, autopilot_ru))
        verb, resource_link = 'post', ''
        headers = self.__rest_headers(verb, 'dbs', resource_link)
        if autopilot_ru > 0:
            settings = {"maxThroughput": autopilot_ru}
            headers['x-ms-cosmos-offer-autopilot-settings'] = json.dumps(settings)
        body = RequestBody.create_db(dbname)
        print(headers)
        print(body)
        url = 'https://{}.documents.azure.com/dbs'.format(self.cosmos_acct)
        return self.__execute_http_request('create_database', verb, url, headers, body)

    def delete_database(self, dbname):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/delete-a-database
        print('delete_database: {}'.format(dbname))
        verb, resource_link = 'delete', 'dbs/{}'.format(dbname)
        headers = self.__rest_headers(verb, 'dbs', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}'.format(self.cosmos_acct, dbname)
        return self.__execute_http_request('delete_database', verb, url, headers)

    def get_database(self, dbname):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/delete-a-database
        print('get_database: {}'.format(dbname))
        verb, resource_link = 'get', 'dbs/{}'.format(dbname)
        headers = self.__rest_headers(verb, 'dbs', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}'.format(
            self.cosmos_acct, dbname)
        return self.__execute_http_request('get_database', verb, url, headers)

    def list_collections(self, dbname):
        # https://docs.microsoft.com/en-us/rest/api/cosmos-db/list-collections
        print('list_collections: {}'.format(dbname))
        verb, resource_link = 'get', 'dbs/{}'.format(dbname)
        headers = self.__rest_headers(verb, 'colls', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}/colls'.format(
            self.cosmos_acct, dbname)
        return self.__execute_http_request('list_collections', verb, url, headers)

    def create_container(self, dbname, cname, ru, pk):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/create-a-collection
        print('create_container: {} {} {} {}'.format(dbname, cname, ru, pk))
        verb, resource_link = 'post', 'dbs/{}'.format(dbname)
        headers = self.__rest_headers(verb, 'colls', resource_link)
        body = RequestBody.create_container(cname, pk)
        if ru > 0:
            headers['x-ms-offer-throughput'] = str(ru)
        url = 'https://{}.documents.azure.com/dbs/{}/colls'.format(
            self.cosmos_acct, dbname)

        print(json.dumps(headers, sort_keys=False, indent=2))
        print(json.dumps(body, sort_keys=False, indent=2))
        print(url)
        return self.__execute_http_request('create_container', verb, url, headers, body)

    def get_container(self, dbname, cname):
        # https://docs.microsoft.com/en-us/rest/api/cosmos-db/get-a-collection
        print('get_container: {} {}'.format(dbname, cname))
        verb, resource_link = 'get', 'dbs/{}/colls/{}'.format(dbname, cname)
        headers = self.__rest_headers(verb, 'colls', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}/colls/{}'.format(
            self.cosmos_acct, dbname, cname)
        return self.__execute_http_request('get_container', verb, url, headers)

    def get_pk_ranges(self, dbname, cname):
        # https://docs.microsoft.com/en-us/rest/api/cosmos-db/get-partition-key-ranges
        # https://docs.microsoft.com/en-us/rest/api/cosmos-db/common-cosmosdb-rest-request-headers
        print('get_pk_ranges: {} {}'.format(dbname, cname))
        verb, resource_link = 'get', 'dbs/{}/colls/{}'.format(dbname, cname)
        headers = self.__rest_headers(verb, 'pkranges', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}/colls/{}/pkranges'.format(
            self.cosmos_acct, dbname, cname)
        return self.__execute_http_request('get_pk_ranges', verb, url, headers)

    def delete_container(self, dbname, cname):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/delete-a-collection
        print('delete_container: {} {}'.format(dbname, cname))
        verb, resource_link = 'delete', 'dbs/{}/colls/{}'.format(dbname, cname)
        headers = self.__rest_headers(verb, 'colls', resource_link)
        url = 'https://{}.documents.azure.com/dbs/{}/colls/{}'.format(
            self.cosmos_acct, dbname, cname)
        return self.__execute_http_request('delete_container', verb, url, headers)

    def list_offers(self):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/querying-offers
        print('list_offers')
        verb, resource_link = 'get', ''
        headers = self.__rest_headers(verb, 'offers', resource_link)
        url = 'https://{}.documents.azure.com/offers'.format(self.cosmos_acct)
        return self.__execute_http_request('list_offers', verb, url, headers)

    def associate_offers(self, dname):
        # Execute three REST calls to obtain info on offers, db, and colls
        r = self.list_offers()
        if r.status_code == 200:
            r = self.get_database(dbname)
        if r.status_code == 200:
            r = self.list_collections(dbname)

        if r.status_code == 200:
            print('info has been gathered for offers, db, colls; now associating...')
            # these 3 files should now exist, created above.  load them into memory.
            offers = self.__load_json_file('tmp/list_offers_200.json')
            db     = self.__load_json_file('tmp/get_database_200.json')
            colls  = self.__load_json_file('tmp/list_collections_200.json')

            associations = list()
            assoc = dict()
            assoc['type'] = 'db'
            assoc['rid']  = db['_rid'] 
            assoc['self'] = db['_self'] 
            assoc['name'] = dbname
            associations.append(assoc)

            for coll in colls['DocumentCollections']:
                assoc = dict()
                assoc['type'] = 'coll'
                assoc['rid']  = coll['_rid'] 
                assoc['self'] = coll['_self'] 
                assoc['name'] = coll['id'] 
                associations.append(assoc)

            for offer in offers['Offers']:
                data = dict()
                data['type'] = 'offer'
                data['id']  = offer['id']
                data['rid'] = offer['resource']
                data['offer'] = offer

                for assoc in associations:
                    if data['rid'] == assoc['self']:
                        assoc['offer'] = offer

            # simple report in terminal
            for assoc in associations:
                if 'offer' in assoc.keys():
                    t = assoc['type']
                    n = assoc['name']
                    s = assoc['self']
                    o = assoc['offer']['id']
                    print('matched; type: {} name: {} self: {} offer id: {}'.format(t, n, s, o))

            self.__write_json_file(associations, 'tmp/offer_associations.json')
            return associations

    def get_offer(self, offer_id):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/get-an-offer
        print('get_offer: {}'.format(offer_id))
        verb, resource_link = 'get', '{}'.format(offer_id)
        headers = self.__rest_headers(verb, 'offers', resource_link)
        url = 'https://{}.documents.azure.com/offers/{}'.format(
            self.cosmos_acct, offer_id)
        return self.__execute_http_request('get_offer', verb, url, headers)

    def set_database_autopilot_ru(self, dbname, ru):
        print('set_database_autopilot_ru: {} {}'.format(dbname, ru))
        associations = self.associate_offers(dbname)

        for a in associations:
            if (a['type'] == 'db') and (a['name'] == dbname):
                offer = a['offer']
                print(json.dumps(offer, sort_keys=False, indent=2))
                offer['content']['offerThroughput'] = ru  # update the offer JSON with new RU 
                print(json.dumps(offer, sort_keys=False, indent=2))
                # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/replace-an-offer
                offer_id = a['offer']['id']
                resource = a['offer']['resource']
                offerResourceId = a['offer']['offerResourceId']
                id  = a['offer']['id']
                rid = a['offer']['_rid']
                body = RequestBody.replace_database_autopilot_offer(
                    ru, resource, offerResourceId, id, rid)
                print(body)
                verb, resource_link = 'put', '{}'.format(offer_id)
                headers = self.__rest_headers(verb, 'offers', resource_link)
                url = 'https://{}.documents.azure.com/offers/{}'.format(
                    self.cosmos_acct, offer_id)
                return self.__execute_http_request('replace_offer', verb, url, headers, body)

    def set_container_ru(self, dbname, cname, ru):
        print('set_container_ru: {} {} {}'.format(dbname, cname, ru))
        associations = self.associate_offers(dbname)

        for a in associations:
            if (a['type'] == 'coll') and (a['name'] == cname):
                offer = a['offer']
                print(json.dumps(offer, sort_keys=False, indent=2))
                offer['content']['offerThroughput'] = ru  # update the offer JSON with new RU 
                print(json.dumps(offer, sort_keys=False, indent=2))
                # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/replace-an-offer
                offer_id = a['offer']['id']
                resource = a['offer']['resource']
                offerResourceId = a['offer']['offerResourceId']
                id  = a['offer']['id']
                rid = a['offer']['_rid']
                body = RequestBody.replace_container_offer(ru, resource, offerResourceId, id, rid)
                print(body)
                verb, resource_link = 'put', '{}'.format(offer_id)
                headers = self.__rest_headers(verb, 'offers', resource_link)
                url = 'https://{}.documents.azure.com/offers/{}'.format(
                    self.cosmos_acct, offer_id)
                return self.__execute_http_request('replace_offer', verb, url, headers, body)

    def get_document(self, dbname, cname, pk, doc_id):
        # See https://docs.microsoft.com/en-us/rest/api/cosmos-db/get-a-document
        print('get_document: {} {} {} {}'.format(dbname, cname, pk, id))
        verb = 'get'
        resource_link = 'dbs/{}/colls/{}/docs/{}'.format(dbname, cname, doc_id)
        #resource_link = doc_id
        headers = self.__rest_headers(verb, 'docs', resource_link)
        headers['x-ms-documentdb-partitionkey'] = '["{}"]'.format(pk)
        url = 'https://{}.documents.azure.com/dbs/{}/colls/{}/docs/{}'.format(
            self.cosmos_acct, dbname, cname, doc_id)
        # https://cjoakimcosmossql.documents.azure.com/dbs/dev/colls/airports/docs/895014e0-1d52-40f6-8ae2-f9dcb0119961
        return self.__execute_http_request('get_document', verb, url, headers)


        # https://{databaseaccount}.documents.azure.com/dbs/{db-id}/colls/{coll-id}/docs/{doc-id}

    # private methods 

    def __rest_headers(self, verb, resource_type, resource_link):
        # https://docs.microsoft.com/en-us/rest/api/cosmos-db/access-control-on-cosmosdb-resources

        rfc_7231_dt = self.__rfc_7231_date()
        string_to_sign = "{}\n{}\n{}\n{}\n\n".format(
            verb, resource_type, resource_link, rfc_7231_dt).lower()
        print("string_to_sign:\n{}---".format(string_to_sign))
        
        # string_to_sign (this works):
        # get
        # colls
        # dbs/dev/colls/airports
        # thu, 13 may 2021 14:46:00 gmt

        # string_to_sign (this works):
        # get
        # pkranges
        # dbs/dev/colls/airports
        # thu, 13 may 2021 14:59:00 gmt


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

    def __rfc_7231_date(self):
        # Return the current timestamp in the following format:
        # Tue, 01 Nov 1994 08:12:31 GMT
        # Tue, 09 Feb 2021 15:59:00 GMT
        return datetime.utcnow().strftime('%a, %d %b %Y %H:%M:00 GMT')

    def __execute_http_request(self, function_name, method, url, headers={}, json_body={}):
        print('===')
        print("invoke: {} {} {}\nheaders: {}\nbody: {}".format(function_name, method.upper(), url, headers, json_body))
        print('---')
        start_epoch = time.time()

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

        end_epoch = time.time()
        elapsed = end_epoch - start_epoch
        print('response: {}  elapsed seconds: {}'.format(r, elapsed))
        if r.status_code in [200, 201]:  # not all responses return a JSON body
            try:
                resp_obj = json.loads(r.text)
                print(json.dumps(resp_obj, sort_keys=False, indent=2))
                print('response: {}'.format(r))
                outfile = 'tmp/{}_{}.json'.format(function_name, r.status_code)
                self.__write_json_file(resp_obj, outfile)
            except Exception as e:
                print("exception processing http response".format(e))
                print(r.text)
        else:
            print(r.text)
        return r

    def __load_json_file(self, infile):
        with open(infile, 'rt') as json_file:
            return json.loads(str(json_file.read()))

    def __write_json_file(self, obj, outfile):
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
            print(client.__rfc_7231_date())

        # database operations 

        elif func == 'list_databases':
            client.list_databases()

        elif func == 'create_database':
            dbname = sys.argv[2]
            autopilot_ru = int(sys.argv[3])
            client.create_database(dbname, autopilot_ru)

        elif func == 'delete_database':
            dbname = sys.argv[2]
            client.delete_database(dbname)

        elif func == 'get_database':
            dbname = sys.argv[2]
            client.get_database(dbname)

        # container operations 

        elif func == 'list_collections':
            dbname = sys.argv[2]
            client.list_collections(dbname)

        elif func == 'create_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            ru     = int(sys.argv[4])
            pk     = sys.argv[5]
            client.create_container(dbname, cname, ru, pk)

        elif func == 'get_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            client.get_container(dbname, cname)

        elif func == 'get_pk_ranges':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            client.get_pk_ranges(dbname, cname)

        elif func == 'delete_container':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            client.delete_container(dbname, cname)

        # offer/throughput operations 

        elif func == 'list_offers':
            client.list_offers()

        elif func == 'get_offer':
            id = sys.argv[2]
            client.get_offer(id)

        elif func == 'associate_offers':
            dbname = sys.argv[2]
            client.associate_offers(dbname)

        elif func == 'set_database_autopilot_ru':
            dbname = sys.argv[2]
            ru     = int(sys.argv[3])
            client.set_database_autopilot_ru(dbname,ru)

        elif func == 'set_container_ru':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            ru     = int(sys.argv[4])
            client.set_container_ru(dbname, cname, ru)

        elif func == 'get_document':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            pk     = sys.argv[4]
            doc_id = sys.argv[5]
            client.get_document(dbname, cname, pk, doc_id)

        elif func == 'help':
            print_options('')

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
