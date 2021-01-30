#!/bin/bash

# Execute cqlsh on local (macOS) workstation vs Azure CosmosDB/Cassandra.
# Chris Joakim, Microsoft, 2020/11/24
# See https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-support

uri=$AZURE_COSMOSDB_CASSANDRA_URI
user=$AZURE_COSMOSDB_CASSANDRA_USER 
pass=$AZURE_COSMOSDB_CASSANDRA_PASS 

#export SSL_CERTFILE=$AZURE_COSMOSDB_CASSANDRA_CERTFILE

export SSL_VERSION=TLSv1_2
export SSL_VALIDATE=false

echo 'connecting to: '$uri
# echo 'user: '$user
# echo 'pass: '$pass

cqlsh $uri 10350 -u $user -p $pass --ssl
