# Azure Synapse Link

## Links

- [Azure Synapse Analytics](https://azure.microsoft.com/en-us/services/synapse-analytics/)
- [What is Azure Synapse Link for Azure Cosmos DB?](https://docs.microsoft.com/en-us/azure/cosmos-db/synapse-link)

---

<p align="center"><img src="img/synapse-analytics-cosmos-db-architecture.png"></p>

---

## Adding Documents with the Python Code in this Repo

```
$ python cosmos_sql.py load_airports dev airports  0 3
{'url': 'https://cjoakimcosmossql.documents.azure.com:443/', 'key': 'qyruLjQ3axmwdWn8wWVxhNUHiq00igkf7RrXKtooXbwtEUDkdsOVwvonB2u0HO0zwLE7kGRYAlvkn0DU2msCPg=='}
{
  "name": "Putnam County Airport",
  "city": "Greencastle",
  "country": "United States",
  "iata_code": "4I7",
  "latitude": "39.6335556",
  "longitude": "-86.8138056",
  "altitude": "842",
  "timezone_num": "-5",
  "timezone_code": "America/New_York",
  "location": {
    "type": "Point",
    "coordinates": [
      -86.8138056,
      39.6335556
    ]
  },
  "pk": "4I7",
  "epoch": 1613581175
}
{'name': 'Putnam County Airport', 'city': 'Greencastle', 'country': 'United States', 'iata_code': '4I7', 'latitude': '39.6335556', 'longitude': '-86.8138056', 'altitude': '842', 'timezone_num': '-5', 'timezone_code': 'America/New_York', 'location': {'type': 'Point', 'coordinates': [-86.8138056, 39.6335556]}, 'pk': '4I7', 'epoch': 1613581175, 'id': 'b16201fd-4def-482b-932d-b1acd7ba8ecb', '_rid': '5IsfAOHCY-S-BQAAAAAAAA==', '_self': 'dbs/5IsfAA==/colls/5IsfAOHCY-Q=/docs/5IsfAOHCY-S-BQAAAAAAAA==/', '_etag': '"0e008be2-0000-0100-0000-602d4b770000"', '_attachments': 'attachments/', '_ts': 1613581175}
last_request_charge: 11.62 activity: c8009880-a01a-48d0-9f64-4ea845b3d696
{
  "name": "Dowagiac Municipal Airport",
  "city": "Dowagiac",
  "country": "United States",
  "iata_code": "C91",
  "latitude": "41.9929342",
  "longitude": "-86.1280125",
  "altitude": "748",
  "timezone_num": "-5",
  "timezone_code": "America/New_York",
  "location": {
    "type": "Point",
    "coordinates": [
      -86.1280125,
      41.9929342
    ]
  },
  "pk": "C91",
  "epoch": 1613581175
}
{'name': 'Dowagiac Municipal Airport', 'city': 'Dowagiac', 'country': 'United States', 'iata_code': 'C91', 'latitude': '41.9929342', 'longitude': '-86.1280125', 'altitude': '748', 'timezone_num': '-5', 'timezone_code': 'America/New_York', 'location': {'type': 'Point', 'coordinates': [-86.1280125, 41.9929342]}, 'pk': 'C91', 'epoch': 1613581175, 'id': 'd6780349-0d6a-46e3-b080-8d89a709ec06', '_rid': '5IsfAOHCY-TABQAAAAAAAA==', '_self': 'dbs/5IsfAA==/colls/5IsfAOHCY-Q=/docs/5IsfAOHCY-TABQAAAAAAAA==/', '_etag': '"0e008ce2-0000-0100-0000-602d4b770000"', '_attachments': 'attachments/', '_ts': 1613581175}
last_request_charge: 11.62 activity: 053bace6-bf7a-411a-b3d9-17b339ba584a
{
  "name": "Cambridge Municipal Airport",
  "city": "Cambridge",
  "country": "United States",
  "iata_code": "CDI",
  "latitude": "39.9750278",
  "longitude": "-81.5775833",
  "altitude": "799",
  "timezone_num": "-5",
  "timezone_code": "America/New_York",
  "location": {
    "type": "Point",
    "coordinates": [
      -81.5775833,
      39.9750278
    ]
  },
  "pk": "CDI",
  "epoch": 1613581175
}
{'name': 'Cambridge Municipal Airport', 'city': 'Cambridge', 'country': 'United States', 'iata_code': 'CDI', 'latitude': '39.9750278', 'longitude': '-81.5775833', 'altitude': '799', 'timezone_num': '-5', 'timezone_code': 'America/New_York', 'location': {'type': 'Point', 'coordinates': [-81.5775833, 39.9750278]}, 'pk': 'CDI', 'epoch': 1613581175, 'id': 'f9612028-2156-4735-8a20-ccb54025e6f9', '_rid': '5IsfAOHCY-TBBQAAAAAAAA==', '_self': 'dbs/5IsfAA==/colls/5IsfAOHCY-Q=/docs/5IsfAOHCY-TBBQAAAAAAAA==/', '_etag': '"0e008de2-0000-0100-0000-602d4b770000"', '_attachments': 'attachments/', '_ts': 1613581175}
last_request_charge: 11.62 activity: 6c16391b-a889-4f2b-a6c4-80e05725337b
(cosmosdb) [~/github/azure-cosmosdb/code/python]$
```

## PySpark Notebook in Azure Synapse to Read the Analytical Column Store

#### Cell 1 

```
# Read from Cosmos DB analytical store into a Spark DataFrame (df) and display 10 rows.
df = spark.read\
    .format("cosmos.olap")\
    .option("spark.synapse.linkedService", "CosmosDbDev")\
    .option("spark.cosmos.container", "airports")\
    .load()
display(df.limit(10))
```

#### Cell 2 

```
# display the observed schema of the observed dataframe 
df.printSchema()

root
 |-- _rid: string (nullable = true)
 |-- _ts: long (nullable = true)
 |-- name: string (nullable = true)
 |-- city: string (nullable = true)
 |-- country: string (nullable = true)
 |-- iata_code: string (nullable = true)
 |-- latitude: string (nullable = true)
 |-- longitude: string (nullable = true)
 |-- altitude: string (nullable = true)
 |-- timezone_num: string (nullable = true)
 |-- timezone_code: string (nullable = true)
 |-- location: struct (nullable = true)
 |    |-- type: string (nullable = true)
 |    |-- coordinates: array (nullable = true)
 |    |    |-- element: double (containsNull = true)
 |-- pk: string (nullable = true)
 |-- epoch: double (nullable = true)
 |-- id: string (nullable = true)
 |-- _etag: string (nullable = true)
```

#### Cell 3 

```
# Count the rows of the dataframe
df.count()

1473
```

#### Cell 4

```
from pyspark.sql.functions import col

timezone_offsets = [-8, -7, -6, -5]
df2 = df.dropna(subset=['iata_code'])
df3 = df2.select('_ts', 'epoch', 'city', 'name', 'altitude') \
    .where(col('timezone_num').isin(timezone_offsets)) \
    .sort(col('_ts').desc())
display(df.limit(10))
```

<p align="center"><img src="img/azure-synapse-pyspark-notebook.png"></p>
