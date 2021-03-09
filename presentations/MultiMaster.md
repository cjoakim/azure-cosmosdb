# CosmosDB MultiMaster

<p align="center"><img src="img/azure-portal-replicate-data-globally.png"></p>

---

## Topics

- [Global Distribution](https://docs.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally)
  - Build highly available apps
  - Build highly responsive apps, low latency
  - [Configure Automatic Failover](https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account#automatic-failover)
  - Choose from among 5 **Consistency Levels**

- [Consistency Levels](https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
  - Strong
  - Bounded Staleness 
  - Session
  - Consistent Prefix
  - Eventual

- [Conflict Resolution](https://docs.microsoft.com/en-us/azure/cosmos-db/global-dist-under-the-hood#conflict-resolution)

- [SDKs for SQL API]
  - [Preferred Regions](https://docs.microsoft.com/en-us/azure/cosmos-db/tutorial-global-distribution-sql-api?tabs=dotnetv2%2Capi-async#preferred-locations)
  - [RetryOptions](https://docs.microsoft.com/en-us/dotnet/api/microsoft.azure.documents.client.connectionpolicy.retryoptions?view=azure-dotnet)
  - [.NET SDK v3](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-dotnet-standard)
  - [Java SDK v4](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-java-v4)
  - [Node.js SDK](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-node)
  - [Python SDK](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-python)
  - [REST](https://docs.microsoft.com/en-us/rest/api/cosmos-db/)

- [CAP Theorem](img/cap_theorem.jpeg)
  - **Consistency**: Every read receives the most recent write or an error
  - **Availability** Every request receives a (non-error) response, without the guarantee that it contains the most recent write
  - **Partition tolerance**: The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes

- [PACELC](https://en.wikipedia.org/wiki/PACELC_theorem)
  - An extension to the CAP Theorem

> It states that in case of **network partitioning (P)** in a distributed computer system, one has to choose between **availability (A)** and **consistency (C)** (as per the CAP theorem), but **else (E)**, even when the system is running normally in the absence of partitions, one has to choose between **latency (L)** and **consistency (C)**.

- [Mark Brown Demo on GitHub](https://github.com/markjbrown/cosmos-global-distribution-demos)
- [Mark Brown Demo Video](https://www.bing.com/videos/search?q=cosmos-global-distribution-demos+video+&&view=detail&mid=E20E6E3CF4E2A83C9A15E20E6E3CF4E2A83C9A15&&FORM=VRDGAR&ru=%2Fvideos%2Fsearch%3Fq%3Dcosmos-global-distribution-demos%2Bvideo%2B%26FORM%3DHDRSC4)
