# 3.08 - Change-Feed

> Change feed in Azure Cosmos DB is a **persistent record of changes to a container in the order they occur**.
> Change feed support in Azure Cosmos DB works by listening to an Azure Cosmos container for any changes. 
> It then outputs the **sorted** list of documents that were changed in the order in which they were modified.
> The persisted changes can be processed asynchronously and incrementally, and the output can be 
> distributed across one or more consumers for **parallel processing**.

See https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed

### Notes:

- It **can be replayed**
- It **can be read from the beginning, or from a given point in time**
- Uses a **leases container** to maintain state, a pointer into the stream
  - Thus the leases container **incurs RUs** as you read the change feed
- Is typically read by **Azure Functions**
- Can also be ready by **SDKs**


## Azure Functions




## Pipelines


## SDKs

Java/Spring example at https://github.com/cjoakim/azure-cosmosdb-changefeed 


---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](3_07_server_side_programming.md) &nbsp; | &nbsp; [next](3_09_ttl.md) &nbsp;
