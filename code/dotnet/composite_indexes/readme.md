# Composite Indexes, Bulk Executor

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-manage-indexing-policy
- https://docs.microsoft.com/en-us/azure/cosmos-db/index-policy#queries-with-a-filter-and-order-by
- https://devblogs.microsoft.com/cosmosdb/new-ways-to-use-composite-indexes/

- https://devblogs.microsoft.com/cosmosdb/introducing-bulk-support-in-the-net-sdk/
- https://docs.microsoft.com/en-us/azure/cosmos-db/tutorial-sql-api-dotnet-bulk-import

---

## DotNet Core Project Setup

```
$ mkdir loader
$ cd loader

$ dotnet --version
5.0.201
$ dotnet new console -o .
$ dotnet add package Microsoft.Azure.Cosmos --version 3.17.1
$ dotnet add package CsvHelper

 <!-- prev: 15.0.8, breaking:21.3.0 -->
$ dotnet list package

    Project 'loader' has the following package references
       [net5.0]:
       Top-level Package             Requested   Resolved
       > CsvHelper                   26.1.0      26.1.0
       > Microsoft.Azure.Cosmos      3.17.1      3.17.1
```

---

## Example Data

### CSV Lines

```
1819,05201,US,Bennington,VT,42.9097220000,-73.1405540000
1830,05301,US,Brattleboro,VT,42.8598240000,-72.6813080000
1859,05405,US,Burlington,VT,44.4776100000,-73.1956320000
1917,05601,US,Montpelier,VT,44.2601000000,-72.5759000000
1983,05753,US,Middlebury,VT,43.9990290000,-73.1761360000

2465,06880,US,Westport,CT,41.1379960000,-73.3441500000
11455,28036,US,Davidson,NC,35.4833060000,-80.7978540000
13528,32082,US,Ponte Vedra Beach,FL,30.1036290000,-81.3701650000
13652,32250,US,Jacksonville Beach,FL,30.2798800000,-81.4164020000
13802,32541,US,Destin,FL,30.3981000000,-86.4558830000
23755,55317,US,Chanhassen,MN,44.8518710000,-93.5542420000
40924,98073,US,Redmond,WA,47.6742000000,-122.1206000000
```

### Corresponding CosmosDB Document

```
{
    "id": "a0180331-ff24-480c-86f7-c862a03da941",
    "rowId": "1859",
    "pk": "VT",
    "postalCode": "05405",
    "countryCode": "US",
    "cityName": "Burlington",
    "stateAbbrv": "VT",
    "latitude": 44.47761,
    "longitude": -73.195632,
    "location": {
        "type": "Point",
        "coordinates": [
            -73.195632,
            44.47761
        ]
    },
    "_rid": "MC8WAOW8uWILAAAAAAAAAA==",
    "_self": "dbs/MC8WAA==/colls/MC8WAOW8uWI=/docs/MC8WAOW8uWILAAAAAAAAAA==/",
    "_etag": "\"4d000932-0000-0100-0000-6071d0b60000\"",
    "_attachments": "attachments/",
    "_ts": 1618071734
}
```

---

## Composite Index Example

See file **index_policies/compidx.json**

```
    "compositeIndexes": [
        [
            {
                "path": "/stateAbbrv",
                "order": "descending"
            },
            {
                "path": "/cityName",
                "order": "descending"
            },
            {
                "path": "/longitude",
                "order": "descending"
            },
            {
                "path": "/latitude",
                "order": "descending"
            }
        ],
        [
            {
                "path": "/pk",
                "order": "descending"
            },
            {
                "path": "/cityName",
                "order": "descending"
            }
        ],
        ...
```

---

## Queries

### Named Query: count_documents

```
connected to container: coll1
ExecuteQuery - sql: SELECT COUNT(1) FROM c
ExecuteQuery - result count: 1, RU: 2.89
{
  "$1": 41032
}

connected to container: coll2
ExecuteQuery - sql: SELECT COUNT(1) FROM c
ExecuteQuery - result count: 1, RU: 2.89
{
  "$1": 41032
}
```

### Named Query: select_four

This query uses the first composite index (listed above).

```
connected to container: coll1
ExecuteQuery - sql: 
  SELECT * from c 
  where c.stateAbbrv = 'CA'
    and CONTAINS(c.cityName, 'San')
    and c.longitude < 117
    and c.latitude < 38.0
  order by c.pk
ExecuteQuery - result count: 354, RU: 32.33

connected to container: coll2
ExecuteQuery - sql: 
  SELECT * from c 
  where c.stateAbbrv = 'CA'
    and CONTAINS(c.cityName, 'San')
    and c.longitude < 117
    and c.latitude < 38.0
  order by c.pk
ExecuteQuery - result count: 354, RU: 24.06
```

**This query costs 34.37% more without the composite index.**

### Named Query: select_four_ordered_two

```
connected to container: coll2
ExecuteQuery - sql:
  SELECT * from c 
  where c.stateAbbrv = 'CA'
    and CONTAINS(c.cityName, 'San')
    and c.longitude < 117
    and c.latitude < 38.0
  order by c.pk, c.cityName
ExecuteQuery - result count: 354, RU: 24.8
```

**This query uses a composite index for both the select and order by clauses.**

### Verify Southern California Results

```
$ cat data/postal_codes_us_filtered.csv | grep CA | grep "Santa Rosa"
39565,95401,US,Santa Rosa,CA,38.4533820000,-122.7813620000
39566,95402,US,Santa Rosa,CA,38.4408000000,-122.7156000000
39567,95403,US,Santa Rosa,CA,38.5028110000,-122.7535360000
39568,95404,US,Santa Rosa,CA,38.4525460000,-122.6403340000
39569,95405,US,Santa Rosa,CA,38.4387240000,-122.6749880000
39570,95406,US,Santa Rosa,CA,38.4408000000,-122.7136000000
39571,95407,US,Santa Rosa,CA,38.3916640000,-122.7511240000
39572,95409,US,Santa Rosa,CA,38.4588400000,-122.6067210000

$ cat tmp/select_four_coll1.txt | grep "Santa Rosa" | wc -l
       0
$ cat tmp/select_four_coll1.txt | grep "San Diego" | wc -l
      79

$ cat tmp/select_four_coll2.txt | grep "Santa Rosa" | wc -l
       0
$ cat tmp/select_four_coll2.txt | grep "San Diego" | wc -l
      79
```