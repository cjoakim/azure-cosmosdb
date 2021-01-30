#!/bin/bash

# Bash shell that defines parameters and environment variables used 
# in this app, and is "sourced" by the other scripts in this repo.
# Chris Joakim, Microsoft, 2021/01/30

# ===

export subscription=$AZURE_SUBSCRIPTION_ID
export user=$USER
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
export cosmos_gremlin_npm_graphname="npm"
export cosmos_gremlin_npm_pk="/pk"
export cosmos_gremlin_npm_ru="500"
export cosmos_gremlin_views_graphname="views"
export cosmos_gremlin_views_pk="/pk"
export cosmos_gremlin_views_ru="500"
#
export cosmos_mongo_region=$primary_region
export cosmos_mongo_locations=""
export cosmos_mongo_rg="cjoakimcosmosmongo"
export cosmos_mongo_acct_name="cjoakimcosmosmongo"
export cosmos_mongo_acct_consistency="Session"    # {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}
export cosmos_mongo_acct_kind="MongoDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_mongo_dbname="dev"
export cosmos_mongo_airports_collname="transportation_nodes"
export cosmos_mongo_airports_shard="pk"
export cosmos_mongo_airports_ru="1000"
#
export cosmos_sql_region=$primary_region
export cosmos_sql_rg="cjoakimcosmossql"
export cosmos_sql_acct_name="cjoakimcosmossql"
export cosmos_sql_acct_consistency="Session"    # {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}
export cosmos_sql_acct_kind="GlobalDocumentDB"  # {GlobalDocumentDB, MongoDB, Parse}
export cosmos_sql_dbname="dev"
export cosmos_sql_db_throughput="5000"
