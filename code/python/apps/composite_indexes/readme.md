# Composite Indexes

## Blog

- See https://devblogs.microsoft.com/cosmosdb/new-ways-to-use-composite-indexes/ 


## Examples for this Repository and Directory

Create two similar containers, **postalcodes1** and **postalcodes2**, each with a partition key of **/pk**.

Then load the same data into each container:

```
$ python main.py load_container dev postalcodes1 data/postal_codes_us_filtered.csv 0 99999
$ python main.py load_container dev postalcodes2 data/postal_codes_us_filtered.csv 0 99999
```

### Sample Document

```
{
  "pk": "NC",
  "original_id": 11270,
  "postal_cd": "27709",
  "country_cd": "US",
  "city_name": "Durham",
  "state_abbrv": "NC",
  "latitude": 35.913747,
  "longitude": -78.86333,
  "epoch": 1617574381
}
```

### postalcodes1 uses this default indexing

```
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [
        {
            "path": "/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/\"_etag\"/?"
        }
    ]
}
```

### postalcodes2 uses this custom indexing with compositeIndexes

```
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {  
            "path":"/*"
        }
    ],
    "excludedPaths": [
        {
            "path": "/\"_etag\"/?"
        }
    ],
    "compositeIndexes":[  
        [  
            {  
                "path":"/pk",
                "order":"ascending"
            },
            {  
                "path":"/country_cd",
                "order":"descending"
            },
            {  
                "path":"/city_name",
                "order":"descending"
            },
            {  
                "path":"/latitude",
                "order":"descending"
            },
            {  
                "path":"/longitude",
                "order":"descending"
            }
        ]
    ]
}
```

### Queries


```
select * from c where c.pk = 'NH' and c.country_cd = 'US' and c.city_name = 'Manchester'
```

The RU cost for this query is **3.03** in **postalcodes1** vs **2.83** in **postalcodes2**


```
select * from c where c.pk = 'NH' and c.country_cd = 'US' and c.city_name = 'Manchester' CONTAINS(c.city_name, "Man")
order by c.pk, c.city_name
```

---


## Examples in the Blog

```
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {  
            "path":"/*"
        }
    ],
    "excludedPaths":[],
    "compositeIndexes":[  
        [  
            {  
                "path":"/name",
                "order":"ascending"
            },
            {  
                "path":"/age",
                "order":"descending"
            }
        ]
    ]
}
```

```
{  
    "automatic":true,
    "indexingMode":"Consistent",
    "includedPaths":[  
        {  
            "path":"/*"
        }
    ],
    "excludedPaths":[],
    "compositeIndexes":[  
        [  
            {  
                "path":"/name",
                "order":"ascending"
            },
            {  
                "path":"/age",
                "order":"ascending"
            }
        ],
        [  
            {  
                "path":"/name",
                "order":"ascending"
            },
            {  
                "path":"/age",
                "order":"descending"
            }
        ]
    ]
}
```
