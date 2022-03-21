# Agenda - 1/31/2022

- CosmosDB/SQL API Vs CosmosDB/Mongo API Vs CosmosDB/Cassandra API
- How CosmosDB Mongo API compares to MongoDB Atlas
- Price comparison between the APIs
- Advice on best practices on: performance, HA/DR, RTO/RPO, etc

```
Chris Joakim
Azure CosmosDB Global Black Belt
chjoakim@microsoft.com
```

### This Presentation URL

https://github.com/cjoakim/azure-cosmosdb/blob/main/presentations/adhoc/tm.md

---

## CosmosDB

- NoSQL database PaaS service
- A single CosmosDB account can be one of: Core SQL, Mongo, Cassandra, Gremlin, etc. APIs
- Very fast reads and writes, point reads especially, performance SLA
- High Availability.  99.99 or 99.999%
- Single Azure Region or Multi-Region with Global Replication
- Scalable Throughput with Request Units (RU).  Autoscale or Manual
- Easy integration with the rest of the Azure Ecosystem

---

## CosmosDB/SQL API Vs CosmosDB/Mongo API Vs CosmosDB/Cassandra API

- https://azure.microsoft.com/en-us/services/cosmos-db

- [Choose an API](https://docs.microsoft.com/en-us/azure/cosmos-db/choose-api)
  - [Core/SQL API](https://docs.microsoft.com/en-us/azure/cosmos-db/choose-api#coresql-api)
    - **Document-oriented, schemaless**
    - Recommended for **Greenfield** apps
    - Use the excellent **Microsoft SDKs for CosmosDB** - DotNet, Java, Python, Node.js, etc
    - Best **integration** into the rest of the Azure Platform, such as:
      - **Azure Synapse Link** for Analytics.  HTAP
        - https://github.com/cjoakim/azure-cosmosdb-synapse-link
        - [Azure Synapse Analytics](https://azure.microsoft.com/en-us/services/synapse-analytics/)
      - Azure Functions and the CosmosDB Change Feed
        - https://github.com/cjoakim/azure-cosmosdb-changefeed
      - Azure Stream Analytics
        - IoT workloads with IotHub or EventHubs
      - Azure Cognitive Search
        - https://github.com/cjoakim/azure-cognitive-search-example
      - Azure Monitor (Log Analytics)

  - [MongoDB API](https://docs.microsoft.com/en-us/azure/cosmos-db/choose-api#api-for-mongodb)
    - **Document-oriented, schemaless**
    - Typically for **lift-and-shift** apps
    - Use the **open-source driver SDKs** (pymongo, etc)
    - Use **mongo tooling** like mongoexport, mongoimport, Studio 3T, and even MatLab

  - [Cassandra API](https://docs.microsoft.com/en-us/azure/cosmos-db/choose-api#cassandra-api)
    - **Column-oriented** schema
    - Cassandra Query Language (CQL), and tools like CQL shell
    - Use the **open-source driver SDKs**

  - [Azure Managed Instance for Apache Cassandra](https://docs.microsoft.com/en-us/azure/managed-instance-apache-cassandra/introduction)
    - Not CosmosDB
    - Deployed automatically as **Virtual Machine scale sets**, in Azure Virtual Networks
    - Enables **Hybrid deployments** - on-prem and Azure

- [Onboarding Best Practices](https://azure.microsoft.com/en-us/resources/azure-cosmos-db-onboarding-best-practices/)

---

## How CosmosDB Mongo API compares to MongoDB Atlas

- Integration with the rest of the Azure Ecosystem
- No tiers.  Highly granular 100-RU increments
- CosmosDB currently supports 4.0 and most of the 4.0 API
- https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb/feature-support-40 

---

## Price comparison between the APIs

- [Pricing](https://azure.microsoft.com/en-us/pricing/details/cosmos-db/)
- [Price/Capacity Calculator](https://cosmos.azure.com/capacitycalculator/)
- [Autoscale](https://docs.microsoft.com/en-us/azure/cosmos-db/provision-throughput-autoscale)

---

## Advice on best practices on: performance, HA/DR, RTO/RPO, etc

- [High Availability](https://docs.microsoft.com/en-us/azure/cosmos-db/high-availability)

>>> To ensure high availability at all times it's recommended to set up your Azure CosmosDB
>>> account with a single write region and at least a second (read) region and enable Service-Managed failover.

- [Continuous Backup Mode - SQL and Mongo](https://docs.microsoft.com/en-us/azure/cosmos-db/restore-account-continuous-backup)
- [Periodic Backup](https://docs.microsoft.com/en-us/azure/cosmos-db/configure-periodic-backup-restore)

---

# Agenda - 3/21/2022

- CosmosDB Costs
- CosmosDB Security

```
Chris Joakim
Azure CosmosDB Global Black Belt
chjoakim@microsoft.com
```

### This Presentation URL

https://github.com/cjoakim/azure-cosmosdb/blob/main/presentations/adhoc/tm.md

---

## Costs

- https://azure.microsoft.com/en-us/pricing/details/cosmos-db/

### Primary Cost Components

0. **There are Zero up-front licensing or initial costs for CosmosDB**
   - Azure PaaS Services: Provision anytime, Change scale anytime, Delete anytime
1. **Provisioned Throughput**
   - https://docs.microsoft.com/en-us/azure/cosmos-db/set-throughput 
   - Be aware of multi-write regions vs single-write and multi-read regions
2. **Consumed Storage (Documents, Indexes)**
3. Backup storage (additional backups, first 2 are free)
4. Regional data distribution - replication, egress
5. Availability zones  (1.25x)
6. Analytical storage transactions (Synapse Link)
7. Dedicated Gateway & Integrated cache (CosmosDB/SQL Integrated Cache)

### Reserved Capacity Discount

- https://docs.microsoft.com/en-us/azure/cosmos-db/cosmos-db-reserved-capacity
- Save up to 65% with a three-year upfront commitment
- Specify the following:
  - Term (1 year or 3 years)
  - Billing frequency (Monthly or Upfront)
  - Throughput Type (RU/s vs multi-region write RU/s)

### Calculators 

- https://cosmos.azure.com/capacitycalculator/
- https://azure.microsoft.com/en-us/pricing/calculator/

### Cost Recommendations

- Don't use CosmosDB as a Data Lake
- Don't delete/define/load collections daily
- Choose your partition keys wisely; query with them often
- Prefer smaller documents for lowest cost updates
  - Product and ProductOnHand example
- Consider Database-Level Shared Throughput
  - eliminates the 400 minimum RU per container issue
  - shares n-number of RUs across the <= 25 containers in a database
- Be aware of multi-write regions vs single-write and multi-read regions
- Subtle Design Differences with MongoDB vs CosmosDB/Mongo API 
  - these are driven by the pricing models of the two databases
  - prefer smaller documents
  - prefer 25 or fewer collections per database
- **Let me help you with your designs**

---

## Security and Compliance

## Compliance

- https://docs.microsoft.com/en-us/azure/compliance/
- https://azure.microsoft.com/en-us/resources/microsoft-azure-compliance-offerings/
- https://docs.microsoft.com/en-us/azure/cosmos-db/compliance

## Security

https://docs.microsoft.com/en-us/azure/cosmos-db/database-security?tabs=sql-api

- **Encryption**
  - Encryption at rest 
  - Encryption in flight
  - Encryption of backups 
  - Encryption Key Types:
    - Service-managed keys - default, created/managed by CosmosDB PaaS service
    - Customer-managed keys or CMK
      - aka "BYOK"
      - https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-setup-cmk
      - You must store customer-managed keys in Azure Key Vault 
   - Client-side Field Level Encryption in 4.2
     - https://devblogs.microsoft.com/cosmosdb/azure-cosmos-db-api-for-mongodb-v4-2-is-here-three-reasons-to-upgrade-now/

- **Key-based Access**
  - Primary and secondary read/write keys
  - Primary and secondary read keys

- **Resource Locks**
  - https://docs.microsoft.com/en-us/azure/cosmos-db/resource-locks
  - Prevent accidental deletion

- **Networking**
  - VNet Service Endpoints
    - https://azure.microsoft.com/en-us/blog/virtual-network-service-endpoints-for-azure-cosmos-db-is-now-generally-available/
    - https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview
    - https://docs.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview
    - https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview
  - Private Endpoints
    - https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-configure-private-endpoints

- **RBAC**
  - https://docs.microsoft.com/en-us/azure/cosmos-db/role-based-access-control
  - Azure RBAC support in Azure Cosmos DB applies to **management plane operations** only

- **Data Plane Operations (Preview)**
  - **Same as MongoDB - roles and users stored in the database**
  - Assign roles to users for collection-level CRUD authorization
