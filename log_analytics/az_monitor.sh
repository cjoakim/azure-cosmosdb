#!/bin/bash

rg_name="cjoakimloganalytics"
la_name="cjoakimla"
la_guid="9b2b96cf-03aa-42b9-95e9-f2b87450e237"

mkdir -p tmp

echo 'az monitor log-analytics workspace list ...'
az monitor log-analytics workspace list \
    --resource-group $rg_name \
    > tmp/la-wsp-list.json

echo 'az monitor log-analytics workspace show ...'
az monitor log-analytics workspace show \
    --resource-group $rg_name \
    --workspace-name $la_name \
    > tmp/la-wsp-show.json

echo 'az monitor log-analytics workspace table list ...' 
az monitor log-analytics workspace table list \
    --resource-group $rg_name \
    --workspace-name $la_name \
    > tmp/la-wsp-table-list.json

# cat tmp/la-wsp-table-list.json | grep name | grep CDB
#     "name": "CDBCassandraRequests",
#     "name": "CDBControlPlaneRequests",
#     "name": "CDBDataPlaneRequests",
#     "name": "CDBGremlinRequests",
#     "name": "CDBMongoRequests",
#     "name": "CDBPartitionKeyRUConsumption",
#     "name": "CDBPartitionKeyStatistics",
#     "name": "CDBQueryRuntimeStatistics",

echo 'az monitor log-analytics workspace table show ...' 
az monitor log-analytics workspace table show \
    --name CDBControlPlaneRequests \
    --resource-group $rg_name \
    --workspace-name $la_name \
    > tmp/la-wsp-table-show-CDBControlPlaneRequests.json

echo 'az monitor log-analytics query 1 (verbose) ...'
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query "CDBControlPlaneRequests" \
    --verbose \
    > tmp/query1.json

echo 'az monitor log-analytics query 2 ...'
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query "CDBDataPlaneRequests" \
    > tmp/query2.json

echo 'az monitor log-analytics query x1 ...'
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query @queries/x1.txt \
    > tmp/query_x1.json

echo 'az monitor log-analytics query x9 ...'
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query @queries/x9.txt \
    > tmp/query_x9.json

echo 'az monitor log-analytics query x10 ...'
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query @queries/x10.txt \
    > tmp/query_x10.json

echo 'az monitor log-analytics query x11 ...'
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query @queries/x11.txt \
    > tmp/query_x11.json

echo 'done'
