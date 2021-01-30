__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.05.28"

import csv
import json
import os


from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub import EventHubConsumerClient

# https://pypi.org/project/azure-eventhub/
# https://pypi.org/project/azure-eventhub/


class EventHub(object):

    def __init__(self, opts):
        self._opts = opts
        self._client = None
        self._mode = None
        self._state = None
        self._verbose = False
        conn_str = opts['conn_str']
        hub_name = opts['hub_name']

        if 'verbose' in opts:
            if opts['verbose'] == True:
                self._verbose = True

        if self.is_consumer():
            consumer_group = opts['consumer_group']
            self._client = EventHubConsumerClient.from_connection_string(
                conn_str, consumer_group, eventhub_name=hub_name)
            self._mode = 'consumer'
            self._state = 'open'
        else:
            self._client = EventHubProducerClient.from_connection_string(
                conn_str, eventhub_name=hub_name)
            self._mode = 'producer'
            self._state = 'open'

        if self._verbose:
            print("EventHub.__init__ client: {}".format(str(type(self._client)))) 

    def send_messages(self, message_list):
        if message_list and len(message_list) > 0:
            batch = self._client.create_batch()
            for msg in message_list:
                    batch.add(EventData(msg))
                    if self._verbose:
                        print('send_messages; added msg to batch: {}'.format(msg))
            #with self._client:
            self._client.send_batch(batch)
            if self._verbose:
                print('send_messages; batch sent')

    def mode(self):
        return str(self._mode)

    def verbose(self):
        return self._verbose

    def state(self):
        return str(self._state)

    def close(self):
        if self._client:
            if self._verbose:
                print('closing...')
            self._client.close()
            self._state = 'closed'
            if self._verbose:
                print('closed')

    def is_consumer(self):
        result = False
        if 'type' in self._opts:
            if self._opts['type'] == 'consumer':
                result = True
        return result 
    