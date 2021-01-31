#!/bin/bash

# Bash script to query a Mongo database - either local or azure
# Use:
# $ ./mongo_query.sh local_airports
# $ ./mongo_query.sh azure_airports
#
# Chris Joakim, Microsoft, 2021/01/31

if [ "$1" == 'local_airports' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongo $MONGODB_LOCAL_URL < mongo/query_local_airports.ddl
fi

if [ "$1" == 'azure_airports' ]
then 
    echo 'connecting to azure at, airports_f: '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    mongo $AZURE_COSMOSDB_MONGODB_CONN_STRING --ssl < mongo/query_azure_airports.ddl
fi
