# 3.03 - Partitioning

CosmosDB uses **partitions** to horizontally distrubute your data across multiple nodes.

## Collections

- A **collection** is a group of documents
- Your database can have 1-to-many collections
- Have **25 or fewer collections pre database to take advantage of Database Level Shared Throughput**
- Again, there is no schema

## Partition Key

- You choose a **partition key attribute name when you create the collection**
- Once a collection is created, the partition key attribute name **can't be changed**
- **pk** is a good choice for a partition key attribute name
  - Gives you the flexibility, over time, to change the partitioning design.  **future-proof**
- It is used to **horizontally distribute** your data in the database
- Strive for a **high-cardinality** partition key attribute **value**
- Strive to use the partition key in many of your queries, as it will be faster cost less RU
- Query-driven design

## Logical Partitions

- A logical partition is the set of all of the documents for a given **partition key value**
- Each logical partition can store **up to 20GB** of data
- 2 MB (UTF-8 length of JSON representation) document size limit

## Physical Partitions

- A physical partition will store the data for 1 or more 
- Each logical partition can store **up to 50GB** of data

## Implementation

- Replica Sets
- Four copies of your data
- Partition Sets (multi-region)

<p align="center"><img src="img/cosmosdb-logical-and-physical-partitions.png" width="90%"></p>

See https://docs.microsoft.com/en-us/azure/cosmos-db/global-dist-under-the-hood

---

## Limits

- https://docs.microsoft.com/en-us/azure/cosmos-db/concepts-limits

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/partitioning-overview


---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](3_02_cosmosdb_non_features.md) &nbsp; | &nbsp; [next](3_04_request_units.md) &nbsp;
