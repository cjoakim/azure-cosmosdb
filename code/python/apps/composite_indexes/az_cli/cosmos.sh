#!/bin/bash

# Bash script with AZ CLI to automate the creation of two similar containers
# for this project.  Different index policies will be used on each.
# Chris Joakim, 2021/04/07
#
# See https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

# az login

export cosmos_sql_rg=$AZURE_COSMOSDB_SQLDB_ACCT
export cosmos_sql_acct_name=$AZURE_COSMOSDB_SQLDB_ACCT
export cosmos_sql_dbname="compidx"
export cosmos_sql_db_autoscale_throughput="4000"

arg_count=$#
processed=0

mkdir -p tmp

delete_db() {
    processed=1
    echo 'deleting cosmos db: '$cosmos_sql_dbname
    az cosmosdb sql database delete \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --name $cosmos_sql_dbname \
        --yes -y \
        > tmp/cosmos_sql_db_delete.json
}

create_db_and_collections() {
    processed=1
    echo 'creating cosmos db: '$cosmos_sql_dbname
    az cosmosdb sql database create \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --name $cosmos_sql_dbname \
        --max-throughput $cosmos_sql_db_autoscale_throughput \
        > tmp/cosmos_sql_db_create.json

    echo 'sleeping 20 before creating collections...'
    sleep 20

    echo 'creating cosmos collection: coll1'
    az cosmosdb sql container create \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --database-name $cosmos_sql_dbname \
        --name coll1 \
        --subscription $AZURE_SUBSCRIPTION_ID \
        --partition-key-path /accountNumber \
        > tmp/cosmos_sql_db_create_coll1.json

    echo 'copying the latest index_policies/compidx.json file to this dir ...'
    cp ../index_policies/compidx.json .

    echo 'creating cosmos collection: coll2'
    az cosmosdb sql container create \
        --resource-group $cosmos_sql_rg \
        --account-name $cosmos_sql_acct_name \
        --database-name $cosmos_sql_dbname \
        --name coll2 \
        --subscription $AZURE_SUBSCRIPTION_ID \
        --partition-key-path /accountNumber \
        --idx @compidx.json \
        > tmp/cosmos_sql_db_create_coll2.json
}

display_usage() {
    echo 'Usage:'
    echo './cosmos.sh delete_db'
    echo './cosmos.sh create_db_and_collections'
}

# ========== "main" logic below ==========

if [ $arg_count -gt 0 ]
then
    for arg in $@
    do
        if [ $arg == "delete_db" ]; then delete_db; fi 
        if [ $arg == "create_db_and_collections" ]; then create_db_and_collections; fi 
    done
fi

if [ $processed -eq 0 ]; then display_usage; fi

echo 'done'
