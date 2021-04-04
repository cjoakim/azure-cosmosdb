# Composite Indexes

## Blog

- See https://devblogs.microsoft.com/cosmosdb/new-ways-to-use-composite-indexes/ 

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

---

## Examples for this Repository and Directory

Create two similar collections, **postalcodes1** and **postalcodes2**, each with a partition key of **/pk**.

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
    "excludedPaths":[],
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

```