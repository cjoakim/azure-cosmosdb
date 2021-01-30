__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.05.28"

import os
import uuid

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from azure.core.exceptions import ResourceExistsError
from azure.core.exceptions import ResourceNotFoundError

# https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python


class Storage(object):

    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string())

    def list_containers(self):
        try:
            return self.blob_service_client.list_containers()
        except ResourceExistsError:
            return list()

    def create_container(self, cname):
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.create_container()
            print('create_container: {}'.format(cname))
        except ResourceExistsError:
            pass

    def delete_container(self, cname):
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.delete_container()
            print('delete_container: {}'.format(cname))
        except ResourceNotFoundError:
            pass

    def list_container(self, cname):
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            return container_client.list_blobs()
        except ResourceExistsError:
            return list()

    def upload_blob(self, local_file_path, cname, blob_name):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data)
            print('upload_blob: {} -> {} {}'.format(local_file_path, cname, blob_name))
        except ResourceNotFoundError:
            pass

    def download_blob(self, cname, blob_name, local_file_path):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            print('download_blob: {} {} -> {}'.format(cname, blob_name, local_file_path))
        except ResourceNotFoundError:
            pass

    def connection_string(self):
        return os.environ['AZURE_STORAGE_CONNECTION_STRING']