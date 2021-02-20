#!/bin/bash

# Bash shell script to mongoimport the transformed data into
# either a local MongoDB or to an Azure CosmosDB w/Mongo API.
# Chris Joakim, Microsoft, 2021/02/20

# create ad-hoc mini files for loading
head -1000 data/mongo/name_basics_small_target.json  > data/mongo/name_basics_mini_target.json
head  -700 data/mongo/title_basics_small_target.json > data/mongo/title_basics_mini_target.json

wc data/mongo/name_basics_mini_target.json
wc data/mongo/title_basics_mini_target.json

if [ "$1" == 'local' ]
then 
    echo 'connecting to '$MONGODB_LOCAL_URL
    sleep 3
    echo 'mongoimport ...'
    mongoimport --db migrate --collection name_basics \
        --file  data/mongo/name_basics_mini_target.json \
        --numInsertionWorkers 1 --batchSize 24 
    sleep 3
    mongoimport --db migrate --collection title_basics \
        --file data/mongo/title_basics_mini_target.json \
        --numInsertionWorkers 1 --batchSize 24 

    sleep 3
    echo 'mongoexport ...'
    mongoexport --db migrate --collection name_basics  --out  data/mongo/name_basics_mini_targetx.json
    sleep 3
    mongoexport --db migrate --collection title_basics --out  data/mongo/title_basics_mini_targetx.json
fi

if [ "$1" == 'azure' ]
then 
    echo 'connecting to azure at '$AZURE_COSMOSDB_MONGODB_CONN_STRING
    sleep 3

    echo 'mongoimport ...'
    mongoimport \
        --host     $AZURE_COSMOSDB_MONGODB_HOST \
        --port     $AZURE_COSMOSDB_MONGODB_PORT \
        --username $AZURE_COSMOSDB_MONGODB_USER \
        --password $AZURE_COSMOSDB_MONGODB_PASS --ssl \
        --db  migrate --collection name_basics \
        --file  data/mongo/name_basics_mini_target.json \
        --numInsertionWorkers 1 --batchSize 24 
    sleep 3
    mongoimport \
        --host     $AZURE_COSMOSDB_MONGODB_HOST \
        --port     $AZURE_COSMOSDB_MONGODB_PORT \
        --username $AZURE_COSMOSDB_MONGODB_USER \
        --password $AZURE_COSMOSDB_MONGODB_PASS --ssl \
        --db  migrate --collection title_basics \
        --file  data/mongo/title_basics_mini_target.json \
        --numInsertionWorkers 1 --batchSize 24 

    # Output:
    # 2021-02-20T09:59:14.848-0500	connected to: cjoakimcosmosmongo.mongo.cosmos.azure.com:10255
    # 2021-02-20T09:59:17.102-0500	[#################.......] migrate.name_basics	224KB/309KB (72.4%)
    # 2021-02-20T09:59:18.041-0500	[########################] migrate.name_basics	309KB/309KB (100.0%)
    # 2021-02-20T09:59:18.041-0500	imported 1000 documents
    # 2021-02-20T09:59:21.896-0500	connected to: cjoakimcosmosmongo.mongo.cosmos.azure.com:10255
    # 2021-02-20T09:59:24.065-0500	[#####################...] migrate.title_basics	207KB/230KB (89.9%)
    # 2021-02-20T09:59:24.490-0500	[########################] migrate.title_basics	230KB/230KB (100.0%)
    # 2021-02-20T09:59:24.490-0500	imported 700 documents
fi
