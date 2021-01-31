#!/bin/bash

# Bash script to initialize a Mongo database - either local or azure;
#
# Use:
# $ ./mongo_init.sh local
# $ ./mongo_init.sh azure
#
# Chris Joakim, Microsoft, 2021/01/31

if [ "$1" == 'local' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongo $MONGODB_LOCAL_URL < mongo/local_init.ddl
fi

if [ "$1" == 'azure' ]
then 
    echo 'connecting to azure at '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    mongo $AZURE_COSMOSDB_MONGODB_CONN_STRING --ssl < mongo/azure_init.ddl
fi
