#!/bin/bash

# Bash script to export a Mongo database
# MongoDB paired utilities:
# - mongodump & mongorestore
# - mongoexport & mongoimport 
# Use:
# $ ./mongo_export.sh local_airports
# $ ./mongo_export.sh azure_airports
#
# Chris Joakim, Microsoft, 2020/04/04

# delete the output dump directory and export file
rm -rf dump/
rm tmp/airports.json

source ../app-config.sh

if [ "$1" == 'local_airports' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongoexport -d $MONGODB_LOCAL_DB -c $MONGODB_LOCAL_COLL --out tmp/airports_local.json
fi

if [ "$1" == 'azure_airports' ]
then 
    echo 'connecting to '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    mongoexport -d $AZURE_COSMOSDB_MONGODB_DBNAME -c "airports" --out tmp/airports_azure.json
fi
