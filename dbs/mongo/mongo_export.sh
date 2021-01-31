#!/bin/bash

# Bash script to export a Mongo database
# MongoDB paired utilities:
# - mongodump & mongorestore
# - mongoexport & mongoimport 
# Use:
# $ ./mongo_export.sh local_airports
# $ ./mongo_export.sh azure_airports
#
# Chris Joakim, Microsoft, 2021/01/31

if [ "$1" == 'local_airports' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    rm tmp/airports_local.json
    mongoexport -d $MONGODB_LOCAL_DB -c $MONGODB_LOCAL_COLL --out tmp/airports_local.json
fi

if [ "$1" == 'azure_airports' ]
then 
    echo 'connecting to '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    rm tmp/airports_azure.json
    mongoexport \
    --host $AZURE_COSMOSDB_MONGODB_HOST \
    --port $AZURE_COSMOSDB_MONGODB_PORT \
    -d $AZURE_COSMOSDB_MONGODB_DBNAME \
    -u $AZURE_COSMOSDB_MONGODB_USER \
    -p $AZURE_COSMOSDB_MONGODB_PASS \
    -c "airports" \
    --ssl \
    --out tmp/airports_azure.json
fi
