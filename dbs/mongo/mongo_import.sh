#!/bin/bash

# Use:
# $ ./mongo_import.sh local_airports
# $ ./mongo_import.sh local_postal_codes_csv
# $ ./mongo_import.sh azure_airports
# $ ./mongo_import.sh azure_postal_codes_csv
#
# Chris Joakim, Microsoft, 2020/10/06

source ../app-config.sh

if [ "$1" == 'local_airports' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongoimport \
    --host $MONGODB_LOCAL_HOST \
    --port $MONGODB_LOCAL_PORT \
    -d $MONGODB_LOCAL_DB \
    -c "airports" \
    data/mongoexport_airports.json
fi

if [ "$1" == 'local_postal_codes_csv' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongoimport \
    --host $MONGODB_LOCAL_HOST \
    --port $MONGODB_LOCAL_PORT \
    -d $MONGODB_LOCAL_DB \
    -c "postal_codes" \
    --headerline --type csv \
    data/postal_codes_nc.csv
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
    --ssl data/mongoexport_airports.json
fi

if [ "$1" == 'azure_postal_codes_csv' ]
then 
    echo 'connecting to '$AZURE_COSMOSDB_MONGODB_HOST
    mongoimport \
    --host $AZURE_COSMOSDB_MONGODB_HOST \
    --port $AZURE_COSMOSDB_MONGODB_PORT \
    -d $AZURE_COSMOSDB_MONGODB_DBNAME \
    -u $AZURE_COSMOSDB_MONGODB_USER \
    -p $AZURE_COSMOSDB_MONGODB_PASS \
    -c "postal_codes" \
    --headerline --type csv \
    --ssl data/postal_codes_nc.csv
fi
