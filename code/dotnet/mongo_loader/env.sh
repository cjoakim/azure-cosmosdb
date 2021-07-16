#!/bin/bash

# This script defines environment variables used in this migration process;
# it is 'sourced' by other scripts in this repo.
# Chris Joakim, Microsoft, July 2021

# These next three directory locations currently point to where the 
# generated artifacts and data are written to; they should be external
# to this GitHub repo.

if [ $HOME == "/home/cjoakim" ];
then
    #echo "we're on a linux vm"
    export M2C_APP_DIR="/home/cjoakim/azure-m2c-wgm-reference-app/reference_app"
else
    #echo "we're on a mac"
    export M2C_APP_DIR=$M2C_REF_APP_DIR  # <-- M2C_REF_APP_DIR already present on workstation
fi
export M2C_APP_ARTIFACTS_DIR=$M2C_APP_DIR"/artifacts"
export M2C_APP_DATA_DIR=$M2C_APP_DIR"/data"

# The generated script type; Windows PowerShell will be added in the future.
export M2C_SHELL_TYPE="bash"

# The Azure Service Principal used by az commands
export M2C_SP_APP_ID=$AZURE_M2C_SP_APP_ID
export M2C_SP_DISPLAY_NAME=$AZURE_M2C_SP_DISPLAY_NAME
export M2C_SP_NAME=$AZURE_M2C_SP_NAME
export M2C_SP_PASSWORD=$AZURE_M2C_SP_PASSWORD
export M2C_SP_TENANT=$AZURE_M2C_SP_TENANT

# Your Azure Subscription used in the migration
export M2C_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID

# The Azure Storage Account used in the Migration process
export M2C_STORAGE_ACCOUNT=$AZURE_M2C_STORAGE_ACCOUNT
export M2C_STORAGE_KEY=$AZURE_M2C_STORAGE_KEY
export M2C_STORAGE_CONNECTION_STRING=$AZURE_M2C_STORAGE_CONNECTION_STRING

# The Source Database.  The values below assume MongoDB Community
# edition running locally as a Docker container.
export M2C_SOURCE_MONGODB_URL="localhost:27017"
export M2C_SOURCE_MONGODB_SSL="false"
export M2C_SOURCE_MONGODB_HOST="localhost"
export M2C_SOURCE_MONGODB_PORT="27017"
export M2C_SOURCE_MONGODB_USER="root"
export M2C_SOURCE_MONGODB_PASS="rootpassword"
# The above localhost:27017 with root/rootpassword point to the MongoDB
# instance running locally in a Docker container, with the reference databases.
# See companion repo https://github.com/cjoakim/mongodb-docker

# Resource Group and Azure Data Factory for the Migration
export M2C_RG=$AZURE_M2C_RG
export M2C_ADF_NAME=$AZURE_M2C_ADF_NAME

# Target CosmosDB/Mongo account
export M2C_COSMOS_MONGODB_ACCT=$AZURE_M2C_COSMOS_MONGO_USER
export M2C_COSMOS_MONGODB_USER=$AZURE_M2C_COSMOS_MONGO_USER
export M2C_COSMOS_MONGODB_PASS=$AZURE_M2C_COSMOS_MONGO_PASS
export M2C_COSMOS_MONGO_CONN_STRING=$AZURE_M2C_COSMOS_MONGO_CONN_STRING

# How we populate CosmosDB/Mongo; either adf or mongoimport
export M2C_COSMOS_LOAD_METHOD="mongoimport"

# mongoimport parameters
export M2C_MONGOIMPORT_NWORKERS="1"
export M2C_MONGOIMPORT_BATCH_SIZE="24"
export M2C_MONGOIMPORT_MODE="upsert"  # [insert|upsert|merge|delete]
