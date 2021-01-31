#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure Cosmos/Mongo DB.
# Chris Joakim, 2021/01/31
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
# See https://docs.microsoft.com/en-us/azure/cosmos-db/scripts/cli/mongodb/create

# See az_cli_login.sh - your terminal needs to be logged-in to Azure, and set to the appropriate subscription.

source ../env.sh

arg_count=$#
processed=0

echo 'creating output directory (git ignored)...'
mkdir -p data/output/

delete() {
    processed=1
    echo 'deleting cosmos rg: '$cosmos_mongo_rg
    az group delete \
        --name $cosmos_mongo_rg \
        --subscription $subscription \
        --yes \
        > data/output/cosmos_mongo_rg_delete.json
}

create() {
    processed=1
    echo 'creating cosmos rg: '$cosmos_mongo_rg
    az group create \
        --location $cosmos_mongo_region \
        --name $cosmos_mongo_rg \
        --subscription $subscription \
        > data/output/cosmos_mongo_rg_create.json

    echo 'creating cosmos acct: '$cosmos_mongo_acct_name
    az cosmosdb create \
        --name $cosmos_mongo_acct_name \
        --resource-group $cosmos_mongo_rg \
        --subscription $subscription \
        --locations regionName=$cosmos_mongo_region failoverPriority=0 isZoneRedundant=False \
        --default-consistency-level $cosmos_mongo_acct_consistency \
        --enable-multiple-write-locations true \
        --kind $cosmos_mongo_acct_kind \
        --capabilities EnableMongo \
        > data/output/cosmos_mongo_acct_create.json

    create_db   
    create_collections
    info
}

recreate_all() {
    processed=1
    delete
    create
    info 
}

recreate_dev_db() {
    processed=1
    delete_db
    sleep 10
    create_db 
    sleep 10 
    create_collections
    info   
}

delete_db() {
    processed=1
    echo 'deleting cosmos db: '$cosmos_mongo_dbname
    az cosmosdb mongodb database delete \
        --resource-group $cosmos_mongo_rg \
        --account-name $cosmos_mongo_acct_name \
        --name $cosmos_mongo_dbname \
        --yes -y \
        > data/output/cosmos_mongo_db_delete.json
}

create_db() {
    processed=1
    echo 'creating cosmos db: '$cosmos_mongo_dbname
    az cosmosdb mongodb database create \
        --resource-group $cosmos_mongo_rg \
        --account-name $cosmos_mongo_acct_name \
        --name $cosmos_mongo_dbname \
        > data/output/cosmos_mongo_db_create.json
}

create_collections() {
    processed=1
    echo 'creating cosmos collection: airports'
    az cosmosdb mongodb collection create \
        --resource-group $cosmos_mongo_rg \
        --account-name $cosmos_mongo_acct_name \
        --database-name $cosmos_mongo_dbname \
        --name 'airports' \
        --shard 'pk' \
        --throughput $cosmos_mongo_airports_ru \
        > data/output/cosmos_mongo_db_create_airports.json

        # --idx @cosmos_mongo_airports_index_policy.json \
}

info() {
    processed=1
    echo 'az cosmosdb show ...'
    az cosmosdb show \
        --name $cosmos_mongo_acct_name \
        --resource-group $cosmos_mongo_rg \
        > data/output/cosmos_mongo_db_show.json

    echo 'az cosmosdb keys list - keys ...'
    az cosmosdb keys list \
        --resource-group $cosmos_mongo_rg \
        --name $cosmos_mongo_acct_name \
        --type keys \
        > data/output/cosmos_mongo_db_keys.json

    echo 'az cosmosdb keys list - connection-strings ...'
    az cosmosdb keys list \
        --resource-group $cosmos_mongo_rg \
        --name $cosmos_mongo_acct_name \
        --type connection-strings \
        > data/output/cosmos_mongo_db_connection_strings.json

    # This command has been deprecated and will be removed in a future release. Use 'cosmosdb keys list' instead.
}

display_usage() {
    echo 'Usage:'
    echo './cosmos_mongo.sh delete'
    echo './cosmos_mongo.sh create'
    echo './cosmos_mongo.sh recreate'
    echo './cosmos_mongo.sh recreate_dev_db'
    echo './cosmos_mongo.sh create_collections'
    echo './cosmos_mongo.sh info'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "delete" ];   then delete; fi 
        if [ $arg == "create" ];   then create; fi 
        if [ $arg == "recreate" ]; then recreate_all; fi 
        if [ $arg == "recreate_dev_db" ]; then recreate_dev_db; fi 
        if [ $arg == "create_collections" ]; then create_collections; fi 
        if [ $arg == "info" ];     then info; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
