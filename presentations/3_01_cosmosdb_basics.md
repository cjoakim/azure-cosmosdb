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
{
   "altitude": "748",
   "city": "Charlotte",
   "country": "United States",
   "iata_code": "CLT",
   "id": "4b98b172-2e9e-11ea-a7b6-7fc29890ecb3",
   "latitude": "35.214",
   "location": {
      "coordinates": [
            -80.943139,
            35.214
      ],
      "type": "Point"
   },
   "longitude": "-80.943139",
   "name": "Charlotte Douglas Intl",
   "pk": "CLT",
   "timezone_code": "America/New_York",
   "timezone_num": "-5",
   "_rid": "LK8RAJxYN85mAQAAAAAAAA==",
   "_self": "dbs/LK8RAA==/colls/LK8RAJxYN84=/docs/LK8RAJxYN85mAQAAAAAAAA==/",
   "_etag": "\"0e028935-0000-0100-0000-60ccf8090000\"",
   "_attachments": "attachments/",
   "_ts": 1624045577
}
```

## Schemaless

- Other than the required **Partition Key** attribute, **there is no schema**
- Your documents don't need to have the same **shape**
- You can, and typically will, store disimilar documents in the same container
- Won't that "break" my SQL queries?  No!


## Collections

- A **collection** is a group of documents
- Your **database** can have 1-to-many collections
- Have **25 or fewer collections pre database to take advantage of Database Level Shared Throughput**
- Again, there is **no schema**


## Optimistic Concurrency Control (OCC)

- Uses the **_etag** system-generated value
- https://docs.microsoft.com/en-us/azure/cosmos-db/database-transactions-optimistic-concurrency


## Sample Queries

```
SELECT * FROM c where c.pk = 'CLT'
SELECT * FROM c where c.pk in ('CLT','ATL,'BDL')
SELECT c.iata_code, c.city, c.name FROM c where c.pk in ('CLT','ATL','BDL')
SELECT c.iata_code, c.city, c.name FROM c where c.pk in ('CLT','ATL','DEN') order by c.name
SELECT COUNT(1) FROM c
```

## Role-Based Access Control (RBAC)

- https://docs.microsoft.com/en-us/azure/cosmos-db/role-based-access-control
- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-setup-rbac
- https://docs.microsoft.com/en-us/azure/cosmos-db/secure-access-to-data
- [Azure Cosmos DB Explorer](https://cosmos.azure.com/?feature.enableAadDataPlane=true)

### Notes

- You can create up to 100 role definitions and 2,000 role assignments per Azure Cosmos DB account.
- The Azure AD token is currently passed as a header with each individual request sent to the Azure Cosmos DB service, increasing the overall payload size.

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](0_table_of_contents.md) &nbsp; | &nbsp; [next](3_02_cosmosdb_non_features.md) &nbsp;
