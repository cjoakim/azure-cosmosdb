# CosmosDB Bulk Loading

This page: https://github.com/cjoakim/azure-cosmosdb/blob/main/presentations/BulkLoading.md

## Bulk Executor Library

- [Bulk Executor Library](https://docs.microsoft.com/en-us/azure/cosmos-db/bulk-executor-overview)
  - High Throughput
  - Handles rate limiting of request, request timeouts, etc
  - Shuffles the data to be loaded into mini-batches by partition key
  - Use this library in your application code, run it on an Azure VM, AKS, ACI
  - [.Net](https://docs.microsoft.com/en-us/azure/cosmos-db/bulk-executor-dot-net)
  - [.Java](https://docs.microsoft.com/en-us/azure/cosmos-db/bulk-executor-java)

## Azure Data Factory (ADF)

- [Copy Activity in Azure Data Factory](https://docs.microsoft.com/en-us/azure/data-factory/connector-azure-cosmos-db)
- Copy data from a source (i.e. - Azure Blob Storage) to a target (i.e. - Azure CosmosDB)
- ADF leverages the above Bulk Executor Library
- Copy to CosmosDB/SQL or CosmosDB/Mongo
- [mongo2cosmos example in this repo](https://github.com/cjoakim/azure-cosmosdb/tree/main/code/python/apps/mongo2cosmos)

## Apache Spark to Azure CosmosDB/SQL connector

- [Spark to Azure Cosmos DB connector](https://docs.microsoft.com/en-us/azure/cosmos-db/spark-connector)
- Run in Azure Databricks or Azure Synapse
- This connector is for the CosmosDB/SQL API
- For Cosmos DB for MongoDB API, use the MongoDB Spark connector
- This connector leverages the above Bulk Executor Library

## Apache Spark to Azure CosmosDB/Mongo connector

- [MongoDB Connector for Spark](See https://docs.mongodb.com/spark-connector/master/)

## CosmosDB Scaling

- Throughput allocated in **Request Units Per Second (RU)**
- Autoscale - range of 10x.
  - For example: 50,000 max to 5,000 low
- Manual Scale - range of 100x ( maxHistoricalManualRu / 100 )
  - For example: 5,000 to 500,000
