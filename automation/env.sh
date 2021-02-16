#!/bin/bash

# Bash shell that defines parameters and environment variables used 
# in this app, and is "sourced" by the other scripts in this repo.
# Chris Joakim, Microsoft, 2021/02/16

# NOTE: PLEASE EDIT ACCOUNT AND RESOURCE-GROUP VALUES IN THIS FILE 
# IF YOU CLONE AND USE THIS REPO (i.e. - rename cjoakim to your name)

# ===

export subscription=$AZURE_SUBSCRIPTION_ID  # refer to my system env var 
export user=$USER                           # refer to my system env var 
export primary_region="eastus"
export secondary_region="westus"
#
export appinsights_region=$primary_region
export appinsights_rg="cjoakimappinsights"
export appinsights_name="cjoakimappinsights"
#
export cosmos_gremlin_region=$primary_region
export cosmos_gremlin_rg="cjoakimcosmosgremlin"
export cosmos_gremlin_acct_name="cjoakimcosmosgremlin"
export cosmos_gremlin_acct_kind="GlobalDocumentDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_gremlin_dbname="dev"
export cosmos_gremlin_npm_ru="400"
export cosmos_gremlin_views_ru="400"
export cosmos_gremlin_amtrak_ru="400"
#
export cosmos_mongo_region=$primary_region
export cosmos_mongo_rg="cjoakimcosmosmongo"
export cosmos_mongo_acct_name="cjoakimcosmosmongo"
export cosmos_mongo_acct_consistency="Session"    # {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}
export cosmos_mongo_acct_kind="MongoDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_mongo_dbname="dev"
export cosmos_mongo_airports_ru="400"
export cosmos_mongo_amtrak_ru="400"
#
export cosmos_sql_region=$primary_region
export cosmos_sql_rg="cjoakimcosmossql"
export cosmos_sql_acct_name="cjoakimcosmossql"
export cosmos_sql_acct_consistency="Session"    # {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}
export cosmos_sql_acct_kind="GlobalDocumentDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_sql_dbname="dev"
export cosmos_sql_db_throughput="4000"
#
export storage_region=$primary_region
export storage_rg="cjoakimstorage"
export storage_name="cjoakimstorage"
export storage_kind="BlobStorage"     # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export storage_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export storage_access_tier="Hot"      # Cool, Hot
#
export synapse_region=$primary_region
export synapse_rg="cjoakimsynapse"
export synapse_name="cjoakimsynapse"
export synapse_stor_kind="StorageV2"       # {BlobStorage, BlockBlobStorage, FileStorage, Storage, StorageV2}]
export synapse_stor_sku="Standard_LRS"     # {Premium_LRS, Premium_ZRS, Standard_GRS, Standard_GZRS, , Standard_RAGRS, Standard_RAGZRS, Standard_ZRS]
export synapse_stor_access_tier="Hot"      # Cool, Hot
export synapse_admin_user=$AZURE_SYNAPSE_USER  # refer to my system env var 
export synapse_admin_pass=$AZURE_SYNAPSE_PASS  # refer to my system env var 
export synapse_fs_name="synapse_acct"
export synapse_sql_pool_name="cjdw200"
export synapse_sql_pool_perf="DW200c" 
export synapse_spark_pool_name="cjspark3s"
export synapse_spark_pool_count="3"
export synapse_spark_pool_size="Small"
