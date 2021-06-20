# 2.02 - Cost Model


## Pricing

These are the components of CosmosDB pricing:

- **Database Operations**
  - Provisioned Throughput Model (Request Units, RUs)
    - Manual Scale, or Autoscale
  - Serverless Model - pay per operation
  - This is typically the most significant cost item

- Consumed Storage

- Backups
  - Two backup copies are provided free
  - Additional copies billed as total GBs of data stored. 

- Dedicated Gateway
  - For Integrated Cache (preview feature)

- Egress Charge
  - For Regional Replication

**Please work with your Azure team to optmize the initial design of your CosmosDB applications.**

#### Links

- [Cosmos DB pricing](https://azure.microsoft.com/en-us/pricing/details/cosmos-db/)
- [Optimize Costs](https://docs.microsoft.com/en-us/azure/cosmos-db/plan-manage-costs)

## Calculators

- [Capacity Calculator](https://cosmos.azure.com/capacitycalculator/)
- [General Azure Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](2_01_cosmosdb_apis.md) &nbsp; | &nbsp; [next](0_table_of_contents.md) &nbsp;
