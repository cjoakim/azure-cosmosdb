#!/bin/bash

# Bash script to load a Mongo database - either local or azure
# Use:
# $ ./mongo_load.sh local_airports
# $ ./mongo_load.sh azure_airports
#
# Chris Joakim, Microsoft, 2021/01/31

if [ "$1" == 'local_airports' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    sleep 3
    mongo $MONGODB_LOCAL_URL < mongo/load_airports.ddl
fi

if [ "$1" == 'azure_airports' ]
then 
    echo 'connecting to azure at '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    sleep 3
    mongo $AZURE_COSMOSDB_MONGODB_CONN_STRING --ssl < mongo/load_airports.ddl
fi
