# 4.05 - Development with SDKs

## Topics

- Programming Language SDKs: .Net, Java, Python, Node.js, and others
- Static vs Dynamic types

---

## .NET SDK v3

- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-dotnet-standard 
- https://github.com/Azure/azure-cosmos-dotnet-v3/tree/master/Microsoft.Azure.Cosmos.Samples/Usage
- https://www.nuget.org/packages/Microsoft.Azure.Cosmos

### Create a Project

```
$ dotnet new console -o MyApp

$cd MyApp 

$ dotnet add package Microsoft.Azure.Cosmos   <-- CosmosDB SDK
$ dotnet add package Azure.Storage.Blobs 
$ dotnet add package CsvHelper

$ dotnet list package
$ dotnet restore
$ dotnet build
$ dotnet run
```

### Code Snippets

#### Imports

```
using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Cosmos.Linq;
```

#### Create a CosmosClient, specifying PreferredRegions

```
string uri = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI");
string key = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_KEY");

IReadOnlyList<string> prefRegionsList = getPreferredRegions();  <-- get list from Environment

CosmosClientOptions options = new CosmosClientOptions {
    ApplicationPreferredRegions = prefRegionsList
};
client = new CosmosClient(uri, key, options);
```

#### Insert some Airport documents, get the status code and RU cost

```
ItemResponse<Airport> response =
    await this.currentContainer.UpsertItemAsync<Airport>(
        airport, new PartitionKey(airport.pk));

log($"status code:    {response.StatusCode}");
log($"request charge: {response.RequestCharge}");
log($"diagnostics:    {response.Diagnostics}");
log($"resource:       {response.Resource}");
```

#### Static Typing example; class Airport

```
ItemResponse<Airport> response =
    await this.currentContainer.UpsertItemAsync<Airport>(
        airport, new PartitionKey(airport.pk));
```

#### Query "Dynamic" Documents

Useful to use this technique when storing dissimilar documents in a container.

[Revisit Retail Example](4_03_relational_to_cosmos_example.md)

```
double totalRequestCharge = 0;
List<dynamic> items = new List<dynamic>();

string sql = "select * from c where c.pk = 'CLT'"

QueryDefinition queryDefinition = new QueryDefinition(sql);

QueryRequestOptions requestOptions = new QueryRequestOptions()
{
    MaxItemCount = maxItems
};

FeedIterator<dynamic> queryResultSetIterator = null;

FeedIterator<dynamic>  queryResultSetIterator =
        this.currentContainer.GetItemQueryIterator<dynamic>(
            queryDefinition,
            requestOptions: requestOptions);

while (queryResultSetIterator.HasMoreResults)
{
    FeedResponse<dynamic> feedResponse =
        await queryResultSetIterator.ReadNextAsync();
    totalRequestCharge += feedResponse.RequestCharge;
    foreach (var item in feedResponse)
    {
        items.Add(item);
    }
}
Console.WriteLine($"queryDocuments - result count: {items.Count}, ru: {totalRequestCharge}");
return items;
```

#### RetryOptions

- https://docs.microsoft.com/en-us/dotnet/api/microsoft.azure.documents.client.connectionpolicy.retryoptions?view=azure-dotnet
- **429 return code = The collection has exceeded the provisioned throughput limit**
- The default retry value is 9
- Example below overrides 9, sets the retry count on 429s to 20

```
ConnectionPolicy connectionPolicy = new ConnectionPolicy();
connectionPolicy.RetryOptions.MaxRetryAttemptsOnThrottledRequests = 20;  
connectionPolicy.RetryOptions.MaxRetryWaitTimeInSeconds = 60;

DocumentClient client = new DocumentClient(
    new Uri("service endpoint"), "auth key", connectionPolicy);
```

**Even with the built-in retry functionality, you should still have a try/catch/finally block in your code to catch and handle all exceptions.**

---

## Java SDK v4

- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-java-v4
- https://mvnrepository.com/artifact/com.azure/azure-cosmos

---

## Python

- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-python
- https://pypi.org/project/azure-cosmos/

### Create a Project

```
... use your preferred version of python3 ...
... create a python virtual environment ...

$ pip install azure-cosmos     <-- CosmosDB SDK 
```

### Code Snippets

See file **code/python/cosmos_sql.py** in this repo.

```
import json
import os
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import azure.cosmos.diagnostics as diagnostics
import azure.cosmos.documents as documents
import azure.cosmos.exceptions as exceptions
import azure.cosmos.partition_key as partition_key

url = os.environ('AZURE_COSMOSDB_SQLDB_URI')
key = os.environ('AZURE_COSMOSDB_SQLDB_KEY')
client = cosmos_client.CosmosClient(url, {'masterKey': key})

client.list_databases()

db = client.create_database(
    id=dbname,
    populate_query_metrics=True,
    response_hook=self._record_diagnostics)

container = db.get_container_client(container_name)

result = container.upsert_doc(obj)

_record_diagnostics = diagnostics.RecordDiagnostics()

doc = container.read_item(
    doc_id,
    partition_key=doc_pk,
    populate_query_metrics=True,
    response_hook=self._record_diagnostics)  <-- callback to update the _record_diagnostics

ru = record_diagnostics.headers['x-ms-request-charge']  
```

---

## Node.js

- https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-node

### Create a Project

```
$ npm install @azure/cosmos 
```

### Code Snippets

```
const CosmosClient = require("@azure/cosmos").CosmosClient;
const format = require('string-format')

// configuration, use environment variables:
const uri     = process.env.AZURE_COSMOSDB_SQLDB_URI;
const key     = process.env.AZURE_COSMOSDB_SQLDB_KEY;
const db      = process.env.AZURE_COSMOSDB_SQLDB_DBNAME;
const coll    = process.env.AZURE_COSMOSDB_SQLDB_COLLNAME;

const client = new CosmosClient({
  endpoint: uri,
  connectionPolicy: {
    preferredLocations: [region1, region2],
  },
  key
});

var querySpec = {
  query: "SELECT c from c where c.pk = 'SUE'"
};

var response = await client
    .database(db)
    .container(coll)
    .items.query(querySpec)
    .fetchAll());
```

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](4_04_local_development.md) &nbsp; | &nbsp; [next](0_table_of_contents.md) &nbsp;
