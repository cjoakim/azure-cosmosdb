# 3.10 - Spatial Support

## GeoJson

See http://geojson.org

- Shapes:
  - Point
  - LineString
  - Polygon
  - MultiPolygon

### Example

Embed a **location object** in your CosmosDB documents.  In this case, a **Point**.

```
{
    "name": "Richardson Stadium",
    "city": "Davidson",
    "state": "NC",
    "tags": [ "davidson college", "track" ],
    "location": {
        "type": "Point",
        "coordinates": [ -80.843276, 35.499648 ]
    }
}
```

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

Alternatively, one of the other **shapes**, such as a **Polygon**.

```
{
    ...
    "location": {
        "type": "Polygon",
        "coordinates": [ [
            [ 31.8, -5 ],
            [ 32, -5 ],
            [ 32, -4.7 ],
            [ 31.8, -4.7 ],
            [ 31.8, -5 ]
        ] ]
    }
}
```

## Query Examples - ST_DISTANCE and ST_WITHIN

See https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-geospatial-intro

Query the documents within **30 Kilometers** from a given GPS point.

```
SELECT *
FROM c
WHERE ST_DISTANCE(c.location, 
    {"type": "Point", "coordinates": [ -80.843276, 35.499648 ] }) < 30000
```


```
SELECT *
FROM Families f
WHERE ST_WITHIN(f.location, {
    "type":"Polygon",
    "coordinates": [[[31.8, -5], [32, -5], [32, -4.7], [31.8, -4.7], [31.8, -5]]]
})
```

The given polygon must be a closed loop; notice that the first GPS location in the coordinates
array is equal to the last GPS location (i.e - [31.8, -5]).


---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](3_09_ttl.md) &nbsp; | &nbsp; [next](3_11_azure_monitor.md) &nbsp;
