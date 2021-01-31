#!/bin/bash

# Bash script with AZ CLI to automate the creation/deletion of my
# Azure Cosmos/SQL DB.
# Chris Joakim, 2021/01/31
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

# See az_cli_login.sh - your terminal needs to be logged-in to Azure, and set to the appropriate subscription.

source ../env.sh

arg_count=$#
processed=0

echo 'creating output directory (git ignored)...'
mkdir -p data/output/

delete() {
    processed=1
    echo 'deleting cosmos rg: '$cosmos_sql_rg
    az group delete \
        --name $cosmos_sql_rg \
        --subscription $subscription \
        --yes \
        > data/output/cosmos_sql_rg_delete.json
}

create() {
    processed=1
    echo 'creating cosmos rg: '$cosmos_sql_rg
    az group create \
        --location $cosmos_sql_region \
        --name $cosmos_sql_rg \
        --subscription $subscription \
        > data/output/cosmos_sql_rg_create.json

    echo 'creating cosmos acct: '$cosmos_sql_acct_name
    az cosmosdb create \
        --name $cosmos_sql_acct_name \
        --resource-group $cosmos_sql_rg \
        --subscription $subscription \
        --locations regionName=$cosmos_sql_region failoverPriority=0 isZoneRedundant=False \
        --default-consistency-level $cosmos_sql_acct_consistency \
        --enable-multiple-write-locations true \
        --enable-analytical-storage true \
        --kind $cosmos_sql_acct_kind \
        > data/output/cosmos_sql_acct_create.json

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
    create_db  
    create_collections
    info   
}

delete_db() {
    processed=1
    echo 'deleting cosmos db: '$cosmos_sql_dbname
    az cosmosdb sql database delete \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --name $cosmos_sql_dbname \
        --yes -y \
        > data/output/cosmos_sql_db_delete.json
}

create_db() {
    processed=1
    echo 'creating cosmos db: '$cosmos_sql_dbname
    az cosmosdb sql database create \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --name $cosmos_sql_dbname \
        --max-throughput $cosmos_sql_db_throughput \
        > data/output/cosmos_sql_db_create.json
}

create_collections() {
    processed=1
    echo 'creating cosmos collection: airports'
    az cosmosdb sql container create \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --database-name $cosmos_sql_dbname \
        --name airports \
        --subscription $subscription \
        --partition-key-path /pk \
        > data/output/cosmos_sql_db_create_airports.json

    echo 'creating cosmos collection: amtrak'
    az cosmosdb sql container create \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --database-name $cosmos_sql_dbname \
        --name amtrak \
        --subscription $subscription \
        --partition-key-path /pk \
        > data/output/cosmos_sql_db_create_amtrak.json
}

info() {
    processed=1
    echo 'az cosmosdb show ...'
    az cosmosdb show \
        --name $cosmos_sql_acct_name \
        --resource-group $cosmos_sql_rg \
        > data/output/cosmos_sql_db_show.json

    echo 'az cosmosdb keys list - keys ...'
    az cosmosdb keys list \
        --resource-group $cosmos_sql_rg \
        --name $cosmos_sql_acct_name \
        --type keys \
        > data/output/cosmos_sql_db_keys.json

    echo 'az cosmosdb keys list - read-only-keys ...'
    az cosmosdb keys list \
        --resource-group $cosmos_sql_rg \
        --name $cosmos_sql_acct_name \
        --type read-only-keys \
        > data/output/cosmos_sql_db_read_only_keys.json

    echo 'az cosmosdb keys list - connection-strings ...'
    az cosmosdb keys list \
        --resource-group $cosmos_sql_rg \
        --name $cosmos_sql_acct_name \
        --type connection-strings \
        > data/output/cosmos_sql_db_connection_strings.json
}

display_usage() {
    echo 'Usage:'
    echo './cosmos_sql.sh delete'
    echo './cosmos_sql.sh create'
    echo './cosmos_sql.sh recreate'
    echo './cosmos_sql.sh recreate_dev_db'
    echo './cosmos_sql.sh info'
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
