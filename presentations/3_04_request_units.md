# 3.04 - Request Units


## What is a Request Unit?

- **Request Unit** is a performance currency abstracting the system resources such as **CPU, IOPS, and Memory** 
- **1.00 RU is the cost of reading a 1.0 KB document by its ID and Partition Key** ( a "point read" )
- In short, **RU is a measure of Throughput**, and is the primary cost component for CosmosDB

- Writing a 1 KB document is approx 5 RU
- Query costs depend on your query and your data
- Azure Portal and our programming language SDKs return you both the data, and the RU charge

## RU Timeframe

- It is a **per second** provisioned throughput; think of it as a **"per second budget"**
- SDK client receives a **HTTP 429 Too many requests** response if you exceed the provisioned throughput
- The SDKs gracefully handle this and **retry up to 9 times**; ( 9 can be configured )

## Provisioned

- You can **manually scale** your CosmosDB containers
- **400 RU** minimum per Container
- You can change this value several ways
  - Azure Portal, Software SDKs, REST API. PowerShell, or az CLI

## Autoscale

- **You specify a maximum value, and CosmosDB will autoscale between that max and 10% of max**
- For example, if you set to 4000 max, then 400 in the min
- Cost per RU is 1.5x higher, but your overall RU consumption will typically be much lower than manual scale
- You can autoscale either **containers** or **databases** (~25 containers)

## Serverless

- Consumption-based cost model; not provisioned
- Can serve thousands of requests per second with no minimum charge and no capacity planning required
- Serverless is best for Dev-Test workloads

## Links

- [Request Units](https://docs.microsoft.com/en-us/azure/cosmos-db/request-units)
- [Serverless](https://docs.microsoft.com/en-us/azure/cosmos-db/serverless)

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](3_03_partitioning.md) &nbsp; | &nbsp; [next](3_05_multi_region.md) &nbsp;
