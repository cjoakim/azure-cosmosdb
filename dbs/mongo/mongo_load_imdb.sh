#!/bin/bash

# Bash script to load a Mongo database - either local or azure
# Use:
# $ ./mongo_load_imdb_.sh local_airports
# $ ./mongo_load_imdb_.sh azure_airports
#
# Chris Joakim, Microsoft, 2021/02/13

if [ "$1" == 'local' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    sleep 3
    mongoimport --db imdb --collection names --file ../../data/imdb/name.basics.mini.tsv.json
    sleep 3
    mongoexport --db imdb --collection names --out ../../data/imdb/name.basics.mini.mongoexport.json
fi

if [ "$1" == 'azure' ]
then 
    echo 'connecting to azure at '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    sleep 3
    mongo $AZURE_COSMOSDB_MONGODB_CONN_STRING --ssl < mongo/load_imdb.ddl
fi
