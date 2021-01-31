#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure Cosmos/Gremlin DB.
# Chris Joakim, 2021/01/30
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
# See https://docs.microsoft.com/en-us/azure/cosmos-db/scripts/cli/gremlin/create

# See az_cli_login.sh - your terminal needs to be logged-in to Azure, and set to the appropriate subscription.

source ../env.sh

arg_count=$#
processed=0

echo 'creating output directory (git ignored)...'
mkdir -p data/output/

delete() {
    processed=1
    echo 'deleting cosmos rg: '$cosmos_gremlin_rg
    az group delete \
        --name $cosmos_gremlin_rg \
        --subscription $subscription \
        --yes \
        > data/output/cosmos_gremlin_rg_delete.json
}

create() {
    processed=1
    echo 'creating cosmos rg: '$cosmos_gremlin_rg
    az group create \
        --location $cosmos_gremlin_region \
        --name $cosmos_gremlin_rg \
        --subscription $subscription \
        > data/output/cosmos_gremlin_rg_create.json

    echo 'creating cosmos acct: '$cosmos_gremlin_acct_name
    az cosmosdb create \
        --name $cosmos_gremlin_acct_name \
        --resource-group $cosmos_gremlin_rg \
        --subscription $subscription \
        --locations regionName=$cosmos_gremlin_region failoverPriority=0 isZoneRedundant=False \
        --capabilities EnableGremlin \
        --default-consistency-level Eventual \
        --enable-multiple-write-locations true \
        > data/output/cosmos_gremlin_acct_create.json

    create_db   
    create_graphs
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
    create_db  
    create_graphs
    info   
}

delete_db() {
    processed=1
    echo 'deleting cosmos db: '$cosmos_gremlin_dbname
    az cosmosdb gremlin database delete \
        --name $cosmos_gremlin_dbname \
        --account-name $cosmos_gremlin_acct_name \
        --resource-group $cosmos_gremlin_rg \
        > data/output/cosmos_gremlin_db_delete.json
}

create_db() {
    processed=1
    echo 'creating cosmos db: '$cosmos_gremlin_dbname
    az cosmosdb gremlin database create \
        --name $cosmos_gremlin_dbname \
        --account-name $cosmos_gremlin_acct_name \
        --resource-group $cosmos_gremlin_rg \
        > data/output/cosmos_gremlin_db_create.json
}

create_graphs() {
    processed=1
    echo 'creating cosmos graph; npm'
    az cosmosdb gremlin graph create \
        --resource-group $cosmos_gremlin_rg \
        --account-name $cosmos_gremlin_acct_name \
        --database-name $cosmos_gremlin_dbname \
        --name 'npm' \
        --partition-key-path '/pk' \
        --throughput $cosmos_gremlin_npm_ru \
        > data/output/cosmos_gremlin_db_create_npm.json

    echo 'creating cosmos graph: views'
    az cosmosdb gremlin graph create \
        --resource-group $cosmos_gremlin_rg \
        --account-name $cosmos_gremlin_acct_name \
        --database-name $cosmos_gremlin_dbname \
        --name 'views' \
        --partition-key-path '/pk' \
        --throughput $cosmos_gremlin_views_ru \
        > data/output/cosmos_gremlin_db_create_views.json
}

info() {
    processed=1
    echo 'az cosmosdb show ...'
    az cosmosdb show \
        --subscription $subscription \
        --resource-group $cosmos_gremlin_rg \
        --name $cosmos_gremlin_acct_name \
        > data/output/cosmos_gremlin_db_show.json

    echo 'az cosmosdb keys list - keys ...'
    az cosmosdb keys list \
        --resource-group $cosmos_gremlin_rg \
        --name $cosmos_gremlin_acct_name \
        --type keys \
        > data/output/cosmos_gremlin_db_keys.json

    echo 'az cosmosdb keys list - connection-strings ...'
    az cosmosdb keys list \
        --resource-group $cosmos_gremlin_rg \
        --name $cosmos_gremlin_acct_name \
        --type connection-strings \
        > data/output/cosmos_gremlin_db_connection_strings.json
}

display_usage() {
    echo 'Usage:'
    echo './cosmos_gremlin.sh delete'
    echo './cosmos_gremlin.sh create'
    echo './cosmos_gremlin.sh recreate'
    echo './cosmos_gremlin.sh recreate_dev_db'
    echo './cosmos_gremlin.sh info'
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
        if [ $arg == "info" ];     then info; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
