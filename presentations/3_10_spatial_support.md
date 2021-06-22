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
