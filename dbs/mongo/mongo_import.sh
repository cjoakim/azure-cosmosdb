#!/bin/bash

# Use:
# $ ./mongo_import.sh local_airports
# $ ./mongo_import.sh azure_airports
#
# Chris Joakim, Microsoft, 2021/01/31

if [ "$1" == 'local_airports' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongoimport \
    --host $MONGODB_LOCAL_HOST \
    --port $MONGODB_LOCAL_PORT \
    -d $MONGODB_LOCAL_DB \
    -c "airports" \
    tmp/airports_azure.json
fi

# Azure Below; Localhost above

if [ "$1" == 'azure_airports' ]
then 
    echo 'connecting to '$AZURE_COSMOSDB_MONGODB_HOST
    mongoimport \
    --host $AZURE_COSMOSDB_MONGODB_HOST \
    --port $AZURE_COSMOSDB_MONGODB_PORT \
    -d $AZURE_COSMOSDB_MONGODB_DBNAME \
    -u $AZURE_COSMOSDB_MONGODB_USER \
    -p $AZURE_COSMOSDB_MONGODB_PASS \
    -c "airports" \
    --ssl tmp/airports_azure.json
fi
