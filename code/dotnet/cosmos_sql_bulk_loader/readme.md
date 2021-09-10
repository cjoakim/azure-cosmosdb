# cosmos_sql_bulk_loader

A simple Console Program to load a CosmosDB/SQL container
using the DotNet C# SDK, and the Bulk Executor functionality.

The input file should be a text file with a JSON-document-per-line.
Each line in the input file will become a CosmosDB document.

## Quick Start

```
$ git clone https://github.com/cjoakim/azure-cosmosdb.git 

$ cd code/dotnet/cosmos_sql_bulk_loader

$ dotnet restore      # downloads the dotnet libraries from NuGet 
$ dotnet build        # compiles the code
...
Build succeeded.
    0 Warning(s)
    0 Error(s)

# "dotnet run" executes the Main method of Program.cs

$ dotnet run bulk_load_container dev travel data/air_travel_departures_10k.json 1
dbname:   dev
cname:    travel
infile:   data/air_travel_departures_10k.json
mbc:      1
uri: https://cjoakimcosmossql.documents.azure.com:443/
LoadContainer - db: dev, container: travel, infile: data/air_travel_departures_10k.json, maxBatchCount: 1
{"id":"cfd95b0f-0b6e-4ed9-8210-6eb3abfde9fd","pk":"MIA:MAO","date":"2001/04/01","year":"2001","month":"4","from_iata":"MIA","to_iata":"MAO","airlineid":"20149","carrier":"PRQ","count":"4","route":"MIA:MAO","from_airport_name":"Miami Intl","from_airport_tz":"America/New_York","from_location":{"type":"Point","coordinates":[-80.290556,25.79325]},"to_airport_name":"Eduardo Gomes Intl","to_airport_country":"Brazil","to_airport_tz":"America/Boa_Vista","to_location":{"type":"Point","coordinates":[-60.049721,-3.038611]},"doc_epoch":1631284457116,"doc_time":"2021/09/10-14:34:17"}
writing batch 1 (500) at 1631284457120

EOJ Totals:
  Database:             dev
  Container:            travel
  Input Filename:       data/air_travel_departures_10k.json
  Max Batch Count:      1
  BulkLoad startEpoch:  1631284456906
  BulkLoad finishEpoch: 1631284459750
  BulkLoad elapsedMs:   2844
  BulkLoad elapsedSec:  2.844
  BulkLoad elapsedMin:  0.0474
  Batch Size:           500
  Batch Count:          1
  Exceptions:           0
  Document/Task count:  500
  Document per Second:  175.8087201125176
```


## Data 

### Input Files


See data/air_travel_departures_10k.json

### Sample CosmosDB Document from the above file

```
{
    "id": "65629b25-f738-44c7-9406-985c50bbbcd4",
    "pk": "BOS:KEF",
    "date": "2007/03/01",
    "year": "2007",
    "month": "3",
    "from_iata": "BOS",
    "to_iata": "KEF",
    "airlineid": "20402",
    "carrier": "GL",
    "count": "1",
    "route": "BOS:KEF",
    "from_airport_name": "General Edward Lawrence Logan Intl",
    "from_airport_tz": "America/New_York",
    "from_location": {
        "type": "Point",
        "coordinates": [
            -71.005181,
            42.364347
        ]
    },
    "to_airport_name": "Keflavik International Airport",
    "to_airport_country": "Iceland",
    "to_airport_tz": "Atlantic/Reykjavik",
    "to_location": {
        "type": "Point",
        "coordinates": [
            -22.605556,
            63.985
        ]
    },
    "doc_epoch": 1631283859866,
    "doc_time": "2021/09/10-14:24:19",
    "_rid": "pVIbAKevu-sDAAAAAAAAAA==",
    "_self": "dbs/pVIbAA==/colls/pVIbAKevu-s=/docs/pVIbAKevu-sDAAAAAAAAAA==/",
    "_etag": "\"1000e5bc-0000-0100-0000-613b6a970000\"",
    "_attachments": "attachments/",
    "_ts": 1631283863
}
```
