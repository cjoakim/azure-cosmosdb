# 4.02 - Design Considerations


## Modeling

- [Data Modeling](https://docs.microsoft.com/en-us/azure/cosmos-db/modeling-data)
- Prefer smaller documents to larger ones
- Prefer write-only documents
- Prefer to update smaller documents, not larger ones
  - Note: Partial Document Updates (in private preview) will alleviate this issue
- Avoid **unbounded arrays** in your documents
- Be aware of the **2MB limit** per document
- Use a generic partition key attribute name (i.e. - **pk**) to give you flexibility over time
  - The partition key attribute name can't be changed after a collection is created
- Use a **high-cardinality partition key** to horizontally distribute and sale your data
- Be aware of the **20GB limit** per logical partition
- Consider using a document type attribute (i.e. - **doctype**) so that you can
  store and identify dissimilar types of documents in the same container
- Use **partition key joins** to efficiently query related documents

---

## Containers

- Start your design with as few containers as possible (i.e. - one)
- Strive for **25 or fewer containers** per database for **database level shared RU Throughput**
- CosmosDB is **schemaless**
  - no schema per collection, unlike relational tables
- You can and often should **store disimilar data in the same container**

### Retail Example

#### Documents in the same Container: order, lineitem, shipment

These related documents have **different shapes** (i.e - doctype)
**but are related** and can be **joined by partition key**.

```
{
  "pk": "XK1123",
  "doctype": "order",
  "orderNumber": "XK1123",
  "customer": "cjoakim",
  ... other order attributes ...
}

{
  "pk": "XK1123",
  "doctype": "lineitem",
  "orderNumber": "XK1123",
  "number": 1,
  "item": {"sku": 123, "cost": 12.44, quantity: 6, "shipping_method": "usps" }
}

{
  "pk": "XK1123",
  "doctype": "lineitem",
  "orderNumber": "XK1123",
  "number": 2,
  "item": {"sku": 456, "cost": 349.99, quantity: 1, "shipping_method": "fedex" }
}

{
  "pk": "XK1123",
  "doctype": "shipment",
  "orderNumber": "XK1123",
  "lineItemNumber": 1,
  "info": {"method": "usps", "status": "shipped", "tracking_number": "x1149qr", quantity: 4 }
}

{
  "pk": "XK1123",
  "doctype": "shipment",
  "orderNumber": "XK1123",
  "lineItemNumber": 2,
  "info": {"method": "fedex", "status": "pending" }
}
```

#### SQL Queries for all or parts of the Order

```
select * from c where c.pk = "XK1123"
select * from c where c.pk = "XK1123" and c.doctype = "order"
select * from c where c.pk = "XK1123" and c.doctype in ("order", "lineitem")
```

### Change-Feed

Considering creating dedicted collection(s) for documents you want to have processed
by a change-feed consumer.

For example, if you have a collection with 1000 upserts per second, but you only
need to process 10 of these with a change-feed consumer, then put those 10
into a dedicated collection so you don't have to ignore the other 990.

---

## Duplicated Data can be Ok

- Depending on your use-cases, **it can be appropriate to duplicate your data**
- There is no **3NF** (Third normal form) in NoSQL
  - https://en.wikipedia.org/wiki/Third_normal_form
- For example, similar documents with different partition keys to optimize the queries
- Storage costs are usually much less signifant than Throughput/RU costs
- Storage costs in 1970 vs today

### Example

Given 100,000 queries per hour for:

- Query product by SKU
- Query product by Model

You could store each product twice, in **two documents**; one for query-by-sku, one for query-by-model

```
{
  "pk": "1048490",
  "sku": "1048490",
  "model": "CMHT51398",
  "description": "CRAFTSMAN 16-oz Smooth Face Steel Head Fiberglass Claw Hammer",
  "price": 11.98,
  "features": [
      "DURABILITY: Overstrike protection where fiberglass handles are most prone to break",
      "IMPROVED GRIP DURING USE: Overmold grip",
      "Includes (1) 16-oz fiberglass hammer"
  ]
}

{
  "pk": "CMHT51398",
  "sku": "1048490",
  "model": "CMHT51398",
  "description": "CRAFTSMAN 16-oz Smooth Face Steel Head Fiberglass Claw Hammer",
  "price": 11.98,
  "features": [
      "DURABILITY: Overstrike protection where fiberglass handles are most prone to break",
      "IMPROVED GRIP DURING USE: Overmold grip",
      "Includes (1) 16-oz fiberglass hammer"
  ]
}
```

Reference: https://www.lowes.com/pd/CRAFTSMAN-16-oz-Smooth-Face-Steel-Head-Fiberglass-Claw-Hammer/1000593895

---

## Indexing

See https://docs.microsoft.com/en-us/azure/cosmos-db/index-policy

- Indexing improves query performance 
- Every Container has an indexing policy, expressed in JSON format
- Default policy indexes every attribute of every document, even nested attributes
- **Two Indexing Modes: Consistent** (typical case), or **None** (for key-value lookups)'
- You can specify which parts of your documents to **include/exclude, by path**
- Best practice is to use indexing to optimize your queries after initial design and development

<p align="center"><img src="img/indexing-settings-in-portal.png" width="90%"></p>

## Composite Indexes

- [Tim Sander Blog](https://devblogs.microsoft.com/cosmosdb/new-ways-to-use-composite-indexes/)

## Links

- [Partial Document Updates](https://azure.microsoft.com/en-us/updates/partial-document-update-for-azure-cosmos-db-in-private-preview/)
- [Real World NoSQL design patterns](https://channel9.msdn.com/Events/Azure-Cosmos-DB/Azure-Cosmos-DB-Conf/Real-World-NoSQL-design-patterns-with-Azure-Cosmos-DB)



[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](4_01_design_process.md) &nbsp; | &nbsp; [next](4_03_relational_to_cosmos_example.md) &nbsp;
