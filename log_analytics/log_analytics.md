# Log Analytics (Azure Monitor)

## Links

- [Monitor CosmosDB](https://docs.microsoft.com/en-us/azure/cosmos-db/monitor-cosmos-db)
- [Examples](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/examples)
- [Basic Queries](https://docs.microsoft.com/en-us/azure/cosmos-db/cosmosdb-monitor-logs-basic-queries)
- [Kusto Query Language quick reference](https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference)

### APIs

- [REST](https://docs.microsoft.com/en-us/rest/api/monitor/)
- [DotNet SDK on NuGet](https://www.nuget.org/packages/Microsoft.Azure.Insights)
- [az CLI](https://docs.microsoft.com/en-us/cli/azure/azure-cli-reference-for-monitor)

This repo has examples of the **az CLI**; it's simple to use.

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

---

## Examples

```
CDBControlPlaneRequests
| where AccountName contains "csl"
| project AccountName, TimeGenerated, OperationName, Result, ActivityId, Type
```

See **az_monitor.sh** and **queries/x1.txt**

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

See **az_monitor.sh** and **queries/x9.txt**

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
  | where todouble(RequestCharge) > 2.0
  | project ActivityId, RequestCharge
  | join kind= inner (
  CDBQueryRuntimeStatistics
  | project ActivityId, QueryText
  ) on $left.ActivityId == $right.ActivityId
  | order by RequestCharge desc
  | limit 100
```

See **az_monitor.sh** and **queries/x10.txt**

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

See **az_monitor.sh** and **queries/x11.txt**

---

## Enable CosmosDB Full Query Text with az rest

See [rest_enable_full_text_query.sh](rest_enable_full_text_query.sh)


```
$ az rest --method PATCH --uri $uri --body '{"properties": {"diagnosticLogSettings": {"enableFullTextQuery": "True"}}}'
```

### Querying Current State 

See [rest_query_full_text_query.sh](rest_query_full_text_query.sh)

Returns a JSON response like the following:

```
{
  "AcctName": "cjoakimcslcosmos",
  "diagnosticLogSettings": {
    "enableFullTextQuery": "True"
  }
}
```

---

## az CLI

See **az_monitor.sh** and **queries/** directory.

### Example: az monitor log-analytics query

```
az monitor log-analytics query \
    --workspace $la_guid \
    --analytics-query @queries/x11.txt \
    > tmp/query_x11.json
```

### Example script: az_monitor.sh

```
$ ./az_monitor.sh
az monitor log-analytics workspace list ...
az monitor log-analytics workspace show ...
az monitor log-analytics workspace table list ...
az monitor log-analytics workspace table show ...
az monitor log-analytics query 1 (verbose) ...
INFO: Command ran in 0.864 seconds (init: 0.082, invoke: 0.781)
az monitor log-analytics query 2 ...
az monitor log-analytics query x1 ...
az monitor log-analytics query x9 ...
az monitor log-analytics query x10 ...
az monitor log-analytics query x11 ...
done
```
