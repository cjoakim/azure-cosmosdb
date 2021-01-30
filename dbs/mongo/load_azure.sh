#!/bin/bash

# Load and query the CosmosDB/Mongo airports collection, and open a
# mongo CLI shell at Azure CosmosDB/Mongo.
#
# Chris Joakim, Microsoft, 2020/10/06

source ../app-config.sh

./mongo_import.sh azure_airports

./mongo_query.sh azure_airports

./mongo_cli.sh azure 
