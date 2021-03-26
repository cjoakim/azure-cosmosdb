# Log Analytics

This page: https://github.com/cjoakim/azure-cosmosdb/blob/main/log_analytics/log_analytics.md

## Links

### General

- https://docs.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-tutorial
- https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/tutorial?pivots=azuremonitor
- https://ms.portal.azure.com/#blade/Microsoft_Azure_Monitoring_Logs/DemoLogsBlade
- https://github.com/microsoft/AzureMonitorCommunity

### CosmosDB

- https://docs.microsoft.com/en-us/azure/cosmos-db/cosmosdb-monitor-resource-logs
- https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-schema#service-specific-schemas
- https://docs.microsoft.com/en-us/azure/cosmos-db/monitor-cosmos-db
- https://docs.microsoft.com/en-us/rest/api/cosmos-db/get-partition-key-ranges
- https://docs.microsoft.com/en-us/azure/cosmos-db/cosmosdb-monitor-resource-logs

## CosmosDB/SQL Account Configuration

<p align="center"><img src="img/cosmossql-diagnostic-settings-in-portal.png" width="95%"></p>

---

## Schema 

- [Top-Level Common schema](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-schema)
- [Service-Specific Schemas](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-schema#service-specific-schemas)
- [Azure CosmosDB Schema]()https://docs.microsoft.com/en-us/azure/cosmos-db/monitor-cosmos-db
- [Azure PostgreSQL Schema](https://docs.microsoft.com/en-us/azure/postgresql/concepts-server-logs#resource-logs)

### Tables

```
AzureDiagnostics 
AzureMetrics
```

### Categories

- [Microsoft.DocumentDB Categories](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-categories#microsoftdocumentdbdatabaseaccounts)

```
CassandraRequests
ControlPlaneRequests
DataPlaneRequests
GremlinRequests
MongoRequests
PartitionKeyRUConsumption
PartitionKeyStatistics
QueryRuntimeStatistics
```

- [Microsoft.DBforPostgreSQL/servers Categories](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-categories#microsoftdbforpostgresqlservers)

```
PostgreSQLLogs
QueryStoreRuntimeStatistics
QueryStoreWaitStatistics
```

For example, using the PartitionKeyStatistics Category:

```
AzureDiagnostics 
| where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="PartitionKeyStatistics"

AzureDiagnostics
| where ResourceProvider =="MICROSOFT.DBFORPOSTGRESQL" 
```

---



## Basic Examples

```
AzureDiagnostics | count 
AzureMetrics | count 
```

### Filter by Boolean expression: where

```
AzureMetrics
| where TimeGenerated > datetime(03-21-2021) and TimeGenerated < datetime(03-21-2027)
| where ResourceProvider == 'MICROSOFT.DOCUMENTDB'
| where Resource == 'CJOAKIMCOSMOSSQL'
```

### Select a subset of columns: project

```
AzureMetrics
| where TimeGenerated > datetime(03-21-2021) and TimeGenerated < datetime(03-21-2027)
| where ResourceProvider == 'MICROSOFT.DOCUMENTDB'
| where Resource == 'CJOAKIMCOSMOSSQL'
| project TimeGenerated, Resource, MetricName
```

### Show n random rows: take

```
AzureMetrics
| where TimeGenerated > datetime(03-21-2021) and TimeGenerated < datetime(03-21-2027)
| where ResourceProvider == 'MICROSOFT.DOCUMENTDB'
| where Resource == 'CJOAKIMCOSMOSSQL'
| project TimeGenerated, Resource, MetricName
| take 22
```

### Order results: sort, top

```
AzureMetrics
| where TimeGenerated > datetime(03-21-2021) and TimeGenerated < datetime(03-21-2027)
| where ResourceProvider == 'MICROSOFT.DOCUMENTDB'
| where Resource == 'CJOAKIMCOSMOSSQL'
| top 10 by TimeGenerated desc
| project TimeGenerated, Resource, MetricName
```


---

## Examples

```
AzureDiagnostics 
| where ResourceProvider=="MICROSOFT.DOCUMENTDB"


AzureDiagnostics 
| where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests"

AzureDiagnostics 
| where toint(duration_s) > 10 and ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests" 
| summarize count() by clientIpAddress_s, TimeGenerated


AzureDiagnostics 
| where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests" 
| project TimeGenerated , duration_s 
| summarize count() by bin(TimeGenerated, 5s)
| render timechart


AzureDiagnostics
| where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests"
| where TimeGenerated >= ago(2h) 
| summarize max(responseLength_s), max(requestLength_s), max(requestCharge_s), count = count() by OperationName, requestResourceType_s, userAgent_s, collectionRid_s, bin(TimeGenerated, 1h)


AzureDiagnostics
| where ResourceProvider=="MICROSOFT.DOCUMENTDB" and Category=="DataPlaneRequests" and todouble(requestCharge_s) > 100.0
| project activityId_g, requestCharge_s
| join kind= inner (
        AzureDiagnostics
        | where ResourceProvider =="MICROSOFT.DOCUMENTDB" and Category == "QueryRuntimeStatistics"
        | project activityId_g, querytext_s
) on $left.activityId_g == $right.activityId_g
| order by requestCharge_s desc
| limit 100


AzureDiagnostics 
| where Category =="ControlPlaneRequests"
| summarize by OperationName

```


---

## Azure Log Analytics REST API

See https://dev.loganalytics.io/ and AAD setup https://dev.loganalytics.io/documentation/Authorization/AAD-Setup

### curl example

```
curl -X POST 'https://api.loganalytics.io/v1/workspaces/DEMO_WORKSPACE/query' -d '{"query": "AzureActivity | summarize count() by Category"}' -H 'x-api-key: DEMO_KEY' -H 'Content-Type: application/json'
```
