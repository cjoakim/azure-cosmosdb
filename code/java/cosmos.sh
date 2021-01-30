#!/bin/bash

# Chris Joakim, Microsoft, 2016/08/14

source classpath

echo 'ZipCodeConsumer ...'
java -classpath $CP org.cjoakim.azure.cosmosdb.CosmosDbUtil

echo 'done'