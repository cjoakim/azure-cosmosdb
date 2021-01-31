#!/bin/bash

# Bash script to open a mongo CLI pointing to either localhost or Azure.
#
# Chris Joakim, Microsoft, 2021/01/31

if [ "$1" == 'local' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    mongo $MONGODB_LOCAL_URL
fi

if [ "$1" == 'azure' ]
then 
    echo 'connecting to: '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    mongo $AZURE_COSMOSDB_MONGODB_CONN_STRING --ssl
fi
