# Composite Indexes

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-manage-indexing-policy
- https://docs.microsoft.com/en-us/azure/cosmos-db/index-policy#queries-with-a-filter-and-order-by
- https://devblogs.microsoft.com/cosmosdb/new-ways-to-use-composite-indexes/ 

---

## Part 2: Design

### First, what does the data look like?

The raw input data is a csv file that looks like this; see file data/postal_codes_us_filtered.csv:

```
id,postal_cd,country_cd,city_name,state_abbrv,latitude,longitude
1,00501,US,Holtsville,NY,40.8154000000,-73.0456000000
```

### Next, how do we want to query it?

We'll primarily want to query by state abbreviation, so we'll use that attribute
as the **partition key**.  To "future proof" the design, we'll call this attribute **/pk**.

#### These are the top queries we anticipate:

```
1) select * from c where c.pk = '<pk>' order by c.city_name desc, c.postal_cd desc

2) select * from c where c.pk  = '<pk>' and c.city_name = 'xxx' order by c.city_name

3) select * from c where c.pk  = '<pk>' and c.city_name like 'xxx'

4) select * from c where c.pk  = '<pk>' and order by c.latitude desc, c.longitude asc

5) We'll also want to query the documents spatially, in GeoJSON format, like this:
    "location": {
        "type": "Point",
        "coordinates": [ -73.0456000000, 40.8154000000 ]
    }

  For example, query all postal codes within 50km of a given GPS location.
```

#### Composite Indexes

Given these queries, we can create these composite indexes for the SELECT and ORDER BY clauses:

```
1) { city_name desc, postal_cd desc } for query 1 order by
2) { pk desc, city_name desc} for queries 2 and 3 select
3) { latitude desc, longitude asc } for query 4 order by
```

Note that the sequence of the fields of the query must match the sequence of the
fields in the composite index.

#### Index Policy JSON

Given the above, we can define the following indexing policy JSON for the collection.
See file **index_policies/compidx.json**.

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
    ],
    "compositeIndexes": [
        [
            {
                "path": "/city_name",
                "order": "descending"
            },
            {
                "path": "/postal_cd",
                "order": "descending"
            }
        ],
        [
            {
                "path": "/pk",
                "order": "descending"
            },
            {
                "path": "/city_name",
                "order": "descending"
            }
        ],
        [
            {
                "path": "/latitude",
                "order": "descending"
            },
            {
                "path": "/longitude",
                "order": "ascending"
            }
        ]
    ]
}
```


### Documents

Transforming the CSV into JSON, the Documents will look like this:

```
{
  "pk": "NY",
  "seq": 1,
  "postal_cd": "00501",
  "country_cd": "US",
  "city_name": "Holtsville",
  "state_abbrv": "NY",
  "latitude": 40.8154,
  "longitude": -73.0456,
  "location": {
    "type": "Point",
    "coordinates": [
      -73.0456,
      40.8154
    ]
  }
}
```

It's ok that there is some duplication of the state_abbrv, latitude, and longitude values,
as this will enabled optimal queries.  Think **query first design**, not about
what your data currently looks like.

---

## Part 2: Running this Project

### Create a CosmosDB/SQL Account

In Azure Portal, create an Azure CosmosDB SQL account.

Alternatively, use an account that already exists, or use PowerShell or the az CLI
to create the account.

### Set Environment Variables

Visit the **Keys Panel** of your Azure CosmosDB SQL account,
and set environment variables in your system/laptop named the following
from the values you see in Azure Portal.  For example:

```
AZURE_COSMOSDB_SQLDB_ACCT=...your-acct...
AZURE_COSMOSDB_SQLDB_URI=https://...your-acct....documents.azure.com:443/
AZURE_COSMOSDB_SQLDB_KEY=R9R...................................................................................==
```

Also add your Azure Subscription ID as an environment variable:

```
AZURE_SUBSCRIPTION_ID=...your-subscription-id...
```

### Create the Database and Collections with the az CLI

This requires that you have the Azure Command Line Tools installed, see 
https://docs.microsoft.com/en-us/cli/azure/install-azure-cli.

Alternatively, use Azure Portal to create the database and two collections
described below.  The indexing policy for coll2 can be pasted into Azure Portal
from the contents of file index_policies/natr_v2.json.

```
$ cd az_cli/

$ az login

$ ./cosmos.sh delete_db

$ ./cosmos.sh create_db_and_collections
```

The last command will create a database in your account named **natr**, with 4000 RU shared throughput,
with collections named **coll1** and **coll2**.  The partition key for both collections is **/accountNumber**.
coll1 uses the default indexing policy, while **coll2 uses the natr_v2.json** indexing policy.

### Create Python Virtual Environment

Create a Python 3 virtual environment with your tool-of-choice, (pyenv, venv, etc.)
then pip install the requirements.txt file.  I use **pyenv** and the **pyenv.sh**
script in this repo.

```
$ ./pyenv.sh
```

