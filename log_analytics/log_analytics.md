# Log Analytics

## Links

- [Monitor CosmosDB](https://docs.microsoft.com/en-us/azure/cosmos-db/monitor-cosmos-db)
- [Examples](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/examples)
- [Basic Queries](https://docs.microsoft.com/en-us/azure/cosmos-db/cosmosdb-monitor-logs-basic-queries)
- [Kusto Query Language quick reference](https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference)

### APIs

- [REST](https://docs.microsoft.com/en-us/rest/api/monitor/)
- [DotNet SDK on NuGet](https://www.nuget.org/packages/Microsoft.Azure.Insights)
- [az CLI](https://docs.microsoft.com/en-us/cli/azure/azure-cli-reference-for-monitor)

---

## Azure Log Analytics REST API

- [Azure Log Analytics REST API](https://dev.loganalytics.io/)
- [AAD setup](https://dev.loganalytics.io/documentation/Authorization/AAD-Setup)

### curl example

```
curl -X POST 'https://api.loganalytics.io/v1/workspaces/DEMO_WORKSPACE/query' -d '{"query": "AzureActivity | summarize count() by Category"}' -H 'x-api-key: DEMO_KEY' -H 'Content-Type: application/json'
```

---

## Schema 

### Tables

- [Tables](https://docs.microsoft.com/en-us/azure/azure-monitor/reference/tables/tables-resourcetype#azure-cosmos-db)

```
AzureActivity
AzureDiagnostics
AzureMetrics
CDBCassandraRequests
CDBControlPlaneRequests
CDBDataPlaneRequests
CDBGremlinRequests
CDBMongoRequests
CDBPartitionKeyRUConsumption
CDBPartitionKeyStatistics
CDBQueryRuntimeStatistics
```

### Categories

```

```

---

## Examples

```
CDBControlPlaneRequests
| where AccountName contains "csl"
| project AccountName, TimeGenerated, OperationName, Result, ActivityId, Type
```

23c10ae8-83c6-4d54-abeb-272871947011

### Azure Metrics

```
AzureMetrics
| summarize Count=count() by MetricName
```

```
AzureMetrics
| where MetricName == "DataUsage" and Resource contains "csl"
```

```
AzureMetrics
| where MetricName == "DocumentCount" and Resource contains "CJOAKIMCOSMOSSQL"
```

### CDBControlPlaneRequests

```
CDBControlPlaneRequests
| summarize Count=count() by OperationName
```

### CDBDataPlaneRequests

```
CDBDataPlaneRequests
| summarize Count=count() by RequestResourceType, RequestResourceId
| order by Count
```

RequestResourceId is Oww-APYSVS8=

### CDBPartitionKeyRUConsumption

Identify the PK Ranges

```
CDBPartitionKeyRUConsumption
| where AccountName contains "csl" and DatabaseName == "demo" and CollectionName == "travel"
| summarize by PartitionKeyRangeId
```

RU consumption by time and pk

```
CDBPartitionKeyRUConsumption 
| summarize total = sum(todouble(RequestCharge)) by DatabaseName, CollectionName, PartitionKey, TimeGenerated 
| order by TimeGenerated asc
```

RU consumption by hottest Logical Partition (partition key)

```
CDBPartitionKeyRUConsumption 
| summarize total = sum(todouble(RequestCharge)) by DatabaseName, CollectionName, PartitionKey, TimeGenerated 
| order by total desc 
```


RU consumption by hottest Physical Partition

```
CDBPartitionKeyRUConsumption 
| summarize total = sum(todouble(RequestCharge)) by DatabaseName, CollectionName, PartitionKey, PartitionKeyRangeId
| order by total desc 
```


### CDBQueryRuntimeStatistics

```
CDBQueryRuntimeStatistics
| where AccountName contains "csl" and DatabaseName == "demo" and CollectionName == "travel"
| project TimeGenerated, PartitionKeyRangeId, QueryText, ActivityId 
| summarize Count=count() by QueryText
```

#### Get the request charges for expensive queries

See https://docs.microsoft.com/en-us/azure/cosmos-db/cosmosdb-monitor-logs-basic-queries

```
CDBDataPlaneRequests
  | where todouble(RequestCharge) > 1.0
  | project ActivityId, RequestCharge
  | join kind= inner (
  CDBQueryRuntimeStatistics
  | project ActivityId, QueryText
  ) on $left.ActivityId == $right.ActivityId
  | order by RequestCharge desc
  | limit 100
```

#### Get the request charges for expensive queries for a db/collection

```
CDBDataPlaneRequests
  | where todouble(RequestCharge) > 1.0
  | project ActivityId, RequestCharge
  | join kind= inner (
  CDBQueryRuntimeStatistics
  | project ActivityId, QueryText, DatabaseName, CollectionName
  ) on $left.ActivityId == $right.ActivityId
  | where CollectionName == "travel"
  | order by RequestCharge desc
  | limit 100
```
