# CosmosDB MultiMaster

## Topics

- [Global Distribution](https://docs.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally)
  - Build highly available apps
  - Build highly responsive apps, low latency
  - [Configure Automatic Failover](https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-manage-database-account#automatic-failover)
  - Choose from among 5 **Consistency Levels**

- [Consistency Levels](https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
  - Strong
  - Bounded staleness 
  - Session
  - Consistent prefix
  - Eventual

- [Conflict Resolution](https://docs.microsoft.com/en-us/azure/cosmos-db/global-dist-under-the-hood#conflict-resolution)

- [CAP Theorem](xxx)

- [PACELC](https://en.wikipedia.org/wiki/PACELC_theorem)
  - An extension to the CAP Theorem

> It states that in case of network **partitioning (P)** in a distributed computer system, one has to choose between availability (A) and consistency (C) (as per the CAP theorem), but else (E), even when the system is running normally in the absence of partitions, one has to choose between latency (L) and consistency (C).


- [Mark Brown Demo on GitHub](https://github.com/markjbrown/cosmos-global-distribution-demos)
- [Mark Brown Demo Video](https://www.bing.com/videos/search?q=cosmos-global-distribution-demos+video+&&view=detail&mid=E20E6E3CF4E2A83C9A15E20E6E3CF4E2A83C9A15&&FORM=VRDGAR&ru=%2Fvideos%2Fsearch%3Fq%3Dcosmos-global-distribution-demos%2Bvideo%2B%26FORM%3DHDRSC4)
