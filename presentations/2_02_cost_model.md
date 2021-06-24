# 2.02 - Cost Model

## Pricing

These are the components of CosmosDB pricing:

- **Database Operations**
  - Provisioned Throughput Model (**Request Units, RUs**)
    - Manual Scale, or Autoscale
  - Serverless Model - pay per operation
  - **This is typically the most significant CosmosDB cost item**

- Consumed Storage

- Backups
  - Two backup copies are provided free
  - Additional copies billed as total GBs of data stored. 

- Dedicated Gateway
  - For Integrated Cache (preview feature)

- Egress Charge
  - For Regional Replication

**Please work with your Azure team to optmize the initial design of your CosmosDB applications.**

**Serverless is best for Dev-Test workloads**


## What is a Request Unit?

- **Request Unit** is a performance currency abstracting the system resources such as CPU, IOPS, and Memory 
- **1.00 RU is the cost of reading a 1.0 KB document by its ID and Partition Key** ( a "point read" )
- Writing a 1 KB document is approx 5 RU
- Query costs depend on your query and your data
- Azure Portal and our programming language SDKs return you both the data, and the RU charge
- In short, **RU is a measure of Throughput**, and is the primary cost component for CosmosDB

## RU Timeframe

- It is a **per second** provisioned throughput; think of it as a **"per second budget"**
- SDK client receives a **HTTP 429 Too many requests** response if you exceed the provisioned throughput
- The SDKs gracefully handle this and **retry up to 9 times**; ( 9 can be configured )

## Heirarchy

```
CosmosDB Account
    Database 1            <-- Throughput can be allocated at the Database level
        Collection 1      <-- Alternatively, throughput can be allocated at the collection level
        Collection 2
    Database 2
        Collection 1
    ...
```

## Links

- [Request Units](https://docs.microsoft.com/en-us/azure/cosmos-db/request-units)
- [Cosmos DB pricing](https://azure.microsoft.com/en-us/pricing/details/cosmos-db/)
- [Optimize Costs](https://docs.microsoft.com/en-us/azure/cosmos-db/plan-manage-costs)
- [Status Codes](https://docs.microsoft.com/en-us/rest/api/cosmos-db/http-status-codes-for-cosmosdb) 
- [Serverless](https://docs.microsoft.com/en-us/azure/cosmos-db/serverless)

## Calculators

- [Capacity Calculator](https://cosmos.azure.com/capacitycalculator/)
- [General Azure Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

## Summary

- CosmosDB is "Serverless"
- Request Units, or Throughput, is the primary cost factor (not storage)

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](2_01_cosmosdb_apis.md) &nbsp; | &nbsp; [next](0_table_of_contents.md) &nbsp;
