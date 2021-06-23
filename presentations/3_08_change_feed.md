# 3.08 - Change-Feed

> Change feed in Azure Cosmos DB is a **persistent record of changes to a container in the order they occur**.
> Change feed support in Azure Cosmos DB works by listening to an Azure Cosmos container for any changes. 
> It then outputs the **sorted** list of documents that were changed in the order in which they were modified.
> The persisted changes can be processed asynchronously and incrementally, and the output can be 
> distributed across one or more consumers for **parallel processing**.

See https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed

### Notes

- It **can be replayed**
- It **can be read from the beginning, or from a given point in time**
- **Delete operations are not currently in the stream**
  - Full Fidelity change-feed is in development
- Uses a **leases container** to maintain state; a pointer into the stream
  - Thus the leases container **incurs RUs** as you read the change feed
- Is typically read by **Azure Functions**
- Can also be ready by **SDKs** (DotNet, Java, Python, Node.js)
- Is supported by the CosmosDB **SQL, Mongo, Cassandra, and Gremlin APIs**

---

## Azure Functions

See https://azure.microsoft.com/en-us/services/functions/

- Azure Functions are **Serverless, Event-Driven Logic**
- Implement in one of several programming languages
- **CosmosDB document insert/update** is one of the many trigger types
- Functions use declaritive **mappings** to point to inputs (i.e. - your CosmosDB account) and outputs
- You Function can be configured to be triggered on **each change** or in **micro batches**

### Pipelines

Some Customers use a **Pipeline** of CosmosDB collections and Azure Functions, like this:

```
CosmosDB Collection 1
  -> Change-Feed Azure Function 1 - Writes to Collection 2

CosmosDB Collection 2
  -> Change-Feed Azure Function 2 - Writes to Collection 3

etc, etc
```

---

## Examples

Java/Spring example at https://github.com/cjoakim/azure-cosmosdb-changefeed 


---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](3_07_server_side_programming.md) &nbsp; | &nbsp; [next](3_09_ttl.md) &nbsp;
