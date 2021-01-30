__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.09.12"

import csv
import json
import os

from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings

from azure.core.exceptions import ResourceExistsError
from azure.core.exceptions import ResourceNotFoundError

# https://github.com/Azure/azure-sdk-for-python
# https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-data-operations-python

class Adl(object):

    def __init__(self):
        url = self.datalake_account_url()
        key = self.datalake_account_key()
        print('url: {}'.format(url))
        print('key: {}'.format(key))
        self.service_client = DataLakeServiceClient(account_url=url, credential=key)
        print(self.service_client)

    def create_fs(self, fsname):
        try:
            fs_client = self.service_client.get_file_system_client(fsname)
            fs_client.create_file_system()
            print('create_fs: {}'.format(fsname))
        except ResourceExistsError:
            pass

    def delete_fs(self, fsname):
        try:
            fs_client = self.service_client.get_file_system_client(fsname)
            fs_client.delete_file_system()
        except ResourceNotFoundError:
            pass

    def filesystem_list(self):
        return self.service_client.list_file_systems()

    def create_dir(self, fsname, dirname):
        try:
            fs_client = self.service_client.get_file_system_client(fsname)
            fs_client.create_directory(dirname)
            print('create_dir: {} in fs: {}'.format(dirname, fsname))
        except:
            pass

    def file_list(self, fsname, dirname):
        try:
            fsc = self.service_client.get_file_system_client(file_system=fsname)
            return fsc.get_paths(path=dirname)
        except Exception as e:
            return list()

    def directory_client(self, fsname, dirname):
        try:
            fs_client = self.service_client.get_file_system_client(fsname)
            return fs_client.get_directory_client(dirname)
        except:
            return None

    def upload_file(self, dir_client, local_path, remote_name, opts={}):
        file_client = dir_client.create_file(remote_name)
        local_file = open(local_path, 'r')
        file_contents = local_file.read()
        print('upload_file, opts: {}'.format(opts))
        # https://docs.microsoft.com/en-us/python/api/azure-storage-file-datalake/azure.storage.filedatalake.contentsettings?view=azure-python
        cs = ContentSettings(**opts)
        file_client.upload_data(file_contents, overwrite=True, content_settings=cs)
        print('upload_file; {} -> {}'.format(local_path, remote_name))

    def download_file(self, dir_client, remote_name, local_path):
        file_client = dir_client.get_file_client(remote_name)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        local_file = open(local_path, 'wb')
        local_file.write(downloaded_bytes)
        local_file.close()
        print('download_file; {} -> {}'.format(remote_name, local_path))

    def datalake_account_url(self):
        storage_account_name = os.environ['AZURE_ADL_ACCOUNT']
        return "{}://{}.dfs.core.windows.net".format("https", storage_account_name)

    def datalake_account_key(self):
        return os.environ['AZURE_ADL_KEY']

    def datalake_account_conn_string(self):
        return os.environ['AZURE_ADL_CONNECTION_STRING']
