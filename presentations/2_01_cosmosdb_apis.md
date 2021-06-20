# 2.01 - CosmosDB APIs


## A Family of NOSQL Databases

<p align="center"><img src="img/azure-cosmos-db-intro.png" width="99%"></p>

#### Common Foundation

- Compute, Storage, Request Units, Monitoring, etc.
- But implements several **wire protocols**, one per **API** type
- **An individual CosmosDB Account is just one of the above APIs** (not all)

---

### Links:

- [Intro](https://docs.microsoft.com/en-us/azure/cosmos-db/introduction)
- [Documentation](https://docs.microsoft.com/en-us/azure/cosmos-db/)
- [NoSQL vs Relational](https://docs.microsoft.com/en-us/azure/cosmos-db/relational-nosql)
- [Learning Path](https://docs.microsoft.com/en-us/learn/paths/work-with-nosql-data-in-azure-cosmos-db/)

---

## SQL API (Document)

- https://docs.microsoft.com/en-us/azure/cosmos-db/create-cosmosdb-resources-portal
- [SQL Queries](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-getting-started)

#### Sample Document 

```
{
  "id": "AndersenFamily",
  "lastName": "Andersen",
  "parents": [
     { "firstName": "Thomas" },
     { "firstName": "Mary Kay"}
  ],
  "children": [
     {
         "firstName": "Henriette Thaulow",
         "gender": "female",
         "grade": 5,
         "pets": [{ "givenName": "Fluffy" }]
     }
  ],
  "address": { "state": "WA", "county": "King", "city": "Seattle" },
  "creationDate": 1431620472,
  "isRegistered": true
}
```

#### Sample Queries 

```
SELECT *
FROM Families f
WHERE f.id = "AndersenFamily"
```

```
SELECT COUNT(1)
FROM c
```

---

## Mongo API

- https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-introduction
- https://www.mongodb.com/

#### Sample Document 

```
TODO
```

---

## Cassandra API

- https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-introduction
- https://cassandra.apache.org/
- [CQL](https://cassandra.apache.org/doc/latest/cql/index.html)

<p align="center"><img src="img/cassandra-keyspace.png" width="90%"></p>

---

## Gremlin/Graph API

- https://docs.microsoft.com/en-us/azure/cosmos-db/graph-introduction
- https://tinkerpop.apache.org/

<p align="center"><img src="img/sample-graph.png" width="90%"></p>

---

## Table API

- https://docs.microsoft.com/en-us/azure/cosmos-db/table-introduction

<p align="center"><img src="img/table-api.png" width="90%"></p>


---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](0_table_of_contents.md) &nbsp; | &nbsp; [next](2_02_cost_model.md) &nbsp;
