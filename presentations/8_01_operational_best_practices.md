# 8.01 - Operational Best Practices 


## Use Azure Monitor

- 

## Deploy to Multi-Regions with Auto Failover 

- Single write region for lower costs
- Use **Auto Failover** (not Manual)
- See https://docs.microsoft.com/en-us/azure/cosmos-db/high-availability


> The best configuration to achieve high availability in case of region outage
> is single write region with service-managed failover.

## Use Synapse Link for Analytics

- Move expensive aggregration queries out of CosmosDB, into Synapse Analytics
- See example repo at: https://github.com/cjoakim/azure-cosmosdb-synapse-link 
