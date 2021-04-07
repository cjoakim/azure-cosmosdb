__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.04.07"

import json
import os

import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import azure.cosmos.diagnostics as diagnostics
import azure.cosmos.documents as documents
import azure.cosmos.exceptions as exceptions
import azure.cosmos.partition_key as partition_key

REQUEST_CHARGE_HEADER = 'x-ms-request-charge'
ACTIVITY_ID_HEADER    = 'x-ms-activity-id'


class Cosmos(object):

    def __init__(self, opts):
        self._opts = opts
        self._dbname = None
        self._dbproxy = None
        self._ctrproxy = None
        self._cname = None
        self._query_metrics = True
        self.reset_record_diagnostics()
        #print(self._opts)
        url = opts['url']
        key = opts['key']
        self._client = cosmos_client.CosmosClient(url, {'masterKey': key})
        # <class 'azure.cosmos.cosmos_client.CosmosClient'>

    def list_databases(self):
        self.reset_record_diagnostics()
        return list(self._client.list_databases())

    def set_db(self, dbname):
        try:
            self.reset_record_diagnostics()
            if self._dbname == dbname:
                pass
            else:
                self._dbproxy = self._client.create_database(
                    id=dbname,
                    populate_query_metrics=self._query_metrics,
                    response_hook=self._record_diagnostics)
                self._dbname = dbname
        except:
            self._dbproxy = self._client.get_database_client(database=dbname)
        return self._dbproxy
        # <class 'azure.cosmos.database.DatabaseProxy'>

    def list_containers(self, proxy=None):
        self.reset_record_diagnostics()
        return list(self._dbproxy.list_containers())

    def create_container(self, cname, pk, throughput):
        try:
            self.reset_record_diagnostics()
            self._ctrproxy = self._dbproxy.create_container(
                id=cname,
                partition_key=partition_key.PartitionKey(path=pk),
                offer_throughput=throughput,
                populate_query_metrics=self._query_metrics,
                response_hook=self._record_diagnostics)
            return self._ctrproxy
            # <class 'azure.cosmos.container.ContainerProxy'>
        except exceptions.CosmosResourceExistsError:
            return self.set_container(cname)
        except:
            return None

    def set_container(self, cname):
        self.reset_record_diagnostics()
        if self._cname == cname:
            pass
        else:
            self._ctrproxy = self._dbproxy.get_container_client(cname)
            self._cname = cname
            # <class 'azure.cosmos.container.ContainerProxy'>
        return self._ctrproxy

    def update_container_throughput(self, cname, throughput):
        self.reset_record_diagnostics()
        self.set_container(cname)
        offer = self._ctrproxy.replace_throughput(
            throughput=int(throughput),
            response_hook=self._record_diagnostics)
        # <class 'azure.cosmos.offer.Offer'>
        return offer

    def get_container_offer(self, cname):
        self.reset_record_diagnostics()
        self.set_container(cname)
        offer = self._ctrproxy.read_offer(
            response_hook=self._record_diagnostics)
        # <class 'azure.cosmos.offer.Offer'>
        return offer

    def delete_container(self, cname):
        try:
            self.reset_record_diagnostics()
            return self._dbproxy.delete_container(
                cname,
                populate_query_metrics=self._query_metrics,
                response_hook=self._record_diagnostics)
        except:
            return None

    def upsert_doc(self, doc):
        try:
            self.reset_record_diagnostics()
            return self._ctrproxy.upsert_item(
                doc,
                populate_query_metrics=self._query_metrics,
                response_hook=self._record_diagnostics)
        except:
            return None

    def delete_doc(self, doc, doc_pk):
        try:
            self.reset_record_diagnostics()
            return self._ctrproxy.delete_item(
                doc,
                partition_key=doc_pk,
                populate_query_metrics=self._query_metrics,
                response_hook=self._record_diagnostics)
        except:
            return None

    def read_doc(self, cname, doc_id, doc_pk):
        try:
            self.set_container(cname)
            self.reset_record_diagnostics()
            return self._ctrproxy.read_item(
                doc_id,
                partition_key=doc_pk,
                populate_query_metrics=self._query_metrics,
                response_hook=self._record_diagnostics)
        except:
            return None

    def query_container(self, cname, sql, xpartition, max_count):
        try:
            self.set_container(cname)
            self.reset_record_diagnostics()
            return self._ctrproxy.query_items(
                query=sql,
                enable_cross_partition_query=xpartition,
                max_item_count=max_count,
                populate_query_metrics=self._query_metrics,
                response_hook=self._record_diagnostics)
        except:
            return None

    # Metrics and Diagnostics

    def enable_query_metrics(self):
        self._query_metrics = True

    def disable_query_metrics(self):
        self._query_metrics = False

    def reset_record_diagnostics(self):
        self._record_diagnostics = diagnostics.RecordDiagnostics()

    def print_record_diagnostics(self):
        # <class 'azure.cosmos.diagnostics.RecordDiagnostics'>
        # headers is an instance of <class 'requests.structures.CaseInsensitiveDict'>
        # and is not JSON serializable
        # headers.keys() is an instance of <class 'collections.abc.KeysView'>
        print('record_diagnostics: {}'.format(self._record_diagnostics.headers))

        print(str(type(self._record_diagnostics.headers)))

        keys = self._record_diagnostics.headers.keys()
        print(str(type(keys)))
        print(keys)

        for header in self._record_diagnostics.headers.items():
            print(header)
            print(str(type(header)))

    def record_diagnostics_headers_dict(self):
        data = dict()
        for header in self._record_diagnostics.headers.items():
            key, val = header  # unpack the header 2-tuple
            data[key] = val
        return data

    def print_last_request_charge(self):
        print('last_request_charge: {} activity: {}'.format(
            self.last_request_charge(),
            self.last_activity_id()))

    def last_request_charge(self):
        if REQUEST_CHARGE_HEADER in self._record_diagnostics.headers:
            return self._record_diagnostics.headers[REQUEST_CHARGE_HEADER]
        else:
            return -1

    def last_activity_id(self):
        if ACTIVITY_ID_HEADER in self._record_diagnostics.headers:
            return self._record_diagnostics.headers[ACTIVITY_ID_HEADER]
        else:
            return None
