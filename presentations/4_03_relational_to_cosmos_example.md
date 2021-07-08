# 4.03 - Relational-to-Cosmos Example

## Retail Example - eCommerce Order, Line Items, Deliveries

```
{
  "pk": "XK1123",             <-- partition key
  "doctype": "order",         <-- the type of document or business object
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
```

In the CosmosDB/SQL API, these documents can be queried efficiently like this:

```
select * from c where c.pk = "XK1123"
select * from c where c.pk = "XK1123" and c.doctype = "order"
select * from c where c.pk = "XK1123" and c.doctype in ("order", "lineitem")
```

---

## GitHub Examples: Adventureworks, etc

<p align="center"><img src="img/AdventureWorksLT-ERD.png" width="50%"></p>

- [cjoakim Adventureworks Azure SQL example](https://github.com/cjoakim/azure-adventureworks-to-cosmos)
- [Mark Brown CosmicWorks example](https://github.com/markjbrown/CosmicWorks)

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/relational-nosql

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](4_02_design_considerations.md) &nbsp; | &nbsp; [next](4_04_local_development.md) &nbsp;
