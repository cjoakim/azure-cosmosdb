# 3.01 - CosmosDB Basics

## PaaS Service

- It's a PaaS service
- There are no servers to patch, or log in to
- Azure manages the Infrastructure, you simply use it
- Azure automatically scales the Infrastructure as you add data


## Note

The 3.xx pages here primarily discuss the **SQL API**

## If it's non-relational, then why is it called the "SQL API"?

Because you query the data with a **SQL Query Syntax**.

## JSON

- Documents are stored in **JSON** (JavaScript Object Notation) format
- Some attributes are added by CosmosDB (_ts)
- 2 MB (UTF-8 length of JSON representation) document size limit

See https://docs.microsoft.com/en-us/azure/cosmos-db/concepts-limits

#### Sample Document

```
TODO
```

## Schemaless

- Other than the required **Partition Key** attribute, **there is no schema**
- Your documents don't need to have the same **shape**
- You can, and typically will, store disimilar documents in the same container
- Won't that "break" my SQL queries?  No


## Collections

- A **collection** is a group of documents
- Your **database** can have 1-to-many collections
- Have **25 or fewer collections pre database to take advantage of Database Level Shared Throughput**
- Again, there is **no schema**


#### Sample Query

```
TODO
```

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](0_table_of_contents.md) &nbsp; | &nbsp; [next](3_02_cosmosdb_non_features.md) &nbsp;
