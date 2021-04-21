# Mongo Modeling and Partitioning in CosmosDB

## Links

- [Azure Cosmos DB's API for MongoDB](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-introduction)
- [Cosmos/Mongo 4.0 Feature Support](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-feature-support-40)
- [Partitioning Overview](https://docs.microsoft.com/en-us/azure/cosmos-db/partitioning-overview)
- [Cosmos/Mongo Indexing](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-indexing)

## Partitioning

<p align="center"><img src="img/cosmosdb-logical-and-physical-partitions.png"></p>

- 20GB max per **logical partition** - the documents in a partition key (pk)
- 50GB max per **physical partition** - automatic partition physical addition and reallocation

## Request Units (RU)

- [Request Units](https://docs.microsoft.com/en-us/azure/cosmos-db/request-units)
- [Request Unit considerations](https://docs.microsoft.com/en-us/azure/cosmos-db/request-units#request-unit-considerations)
- [x-ms-request-charge](https://docs.microsoft.com/en-us/rest/api/cosmos-db/common-cosmosdb-rest-response-headers)

## Design

- 2MB max doc size
- Prefer smaller documents
- Consider refactoring embedded arrays into separate documents
- Store disimilar documents in the same container; use a **doctype** attribute to distinguish them
- **Point-Reads** are the most efficient and lowest cost
- Query by partition key as much as possible
- Use **partition key joins** to aggregate documents efficiently
- Know the costs of your queries during development; x-ms-request-charge
- Autoscaled databases - 25 containers/collections max

### Example - eCommerce Order, Line Items, Deliveries

```
{
  "pk": "XK1123",
  "doctype": "order",
  "orderNumber": "XK1123",
  ... order attributes ...
}

{
  "pk": "XK1123",
  "doctype": "lineitem",
  "orderNumber": "XK1123",
  "lineItem": 1,
  ... lineitem attributes ...
}

{
  "pk": "XK1123",
  "doctype": "lineitem",
  "orderNumber": "XK1123",
  "lineItem": 2,
  ... lineitem attributes ...
}

{
  "pk": "XK1123",
  "doctype": "delivery",
  "orderNumber": "XK1123",
  "lineItem": 1,
  "deliveryNumber": 1,
  ... delivery attributes ...
}

select * from c where c.pk = "XK1123"
select * from c where c.pk = "XK1123" and c.doctype = "order"
select * from c where c.pk = "XK1123" and c.doctype in ("order", "lineitem")
```
