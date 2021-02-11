#!/bin/bash

db='dev2'
coll='airports'

rm tmp/*.*

python cosmos_sql_rest_client.py list_databases

python cosmos_sql_rest_client.py list_offers

python cosmos_sql_rest_client.py get_database $db

python cosmos_sql_rest_client.py list_collections $db

python cosmos_sql_rest_client.py get_container $db $coll

echo ''
echo 'done; see the REST response files in the tmp/ directory'
ls -al tmp/ | grep json
