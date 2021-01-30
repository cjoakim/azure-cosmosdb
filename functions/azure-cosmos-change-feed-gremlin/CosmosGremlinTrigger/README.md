


```
$ dotnet restore
$ dotnet build
...
Build succeeded.
    0 Warning(s)
    0 Error(s)

```

```
$ func start
Microsoft (R) Build Engine version 16.8.0+126527ff1 for .NET
Copyright (C) Microsoft Corporation. All rights reserved.

  Determining projects to restore...
  All projects are up-to-date for restore.
  CosmosGremlinTrigger -> .../CosmosGremlinTrigger/bin/output/bin/CosmosGremlinTrigger.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)
Time Elapsed 00:00:01.87

Azure Functions Core Tools
Core Tools Version:       3.0.2996 Commit hash: c54cdc36323e9543ba11fb61dd107616e9022bba
Function Runtime Version: 3.0.14916.0

Functions:
	CosmosGremlinTrigger: cosmosDBTrigger

For detailed output, run func with --verbose flag.
[2021-01-21T19:03:38.416Z] Executing 'CosmosGremlinTrigger' (Reason='New changes on collection npm at 2021-01-21T19:03:38.3768270Z', Id=eec855bc-b7ca-48d2-88d3-5d325d10eb91)
[2021-01-21T19:03:38.427Z] Documents modified 3
[2021-01-21T19:03:38.427Z] Document Id @azure|event-hubs
[2021-01-21T19:03:38.435Z] {
[2021-01-21T19:03:38.435Z]   "AttachmentsLink": "dbs/uY8bAA==/colls/uY8bALgik0U=/docs/uY8bALgik0UdAAAAAAAAAA==/attachments/",
[2021-01-21T19:03:38.435Z]   "TimeToLive": null,
[2021-01-21T19:03:38.435Z]   "Id": "@azure|event-hubs",
[2021-01-21T19:03:38.435Z]   "ResourceId": "uY8bALgik0UdAAAAAAAAAA==",
[2021-01-21T19:03:38.435Z]   "SelfLink": "dbs/uY8bAA==/colls/uY8bALgik0U=/docs/uY8bALgik0UdAAAAAAAAAA==/",
[2021-01-21T19:03:38.435Z]   "AltLink": "dbs/dev/colls/npm/docs/@azure|event-hubs",
[2021-01-21T19:03:38.435Z]   "Timestamp": "2021-01-21T18:55:00Z",
[2021-01-21T19:03:38.435Z]   "ETag": "\u00225e0059f1-0000-0100-0000-6009ce040000\u0022"
[2021-01-21T19:03:38.435Z] }
[2021-01-21T19:03:38.435Z] Document Id @azure|ms-rest-azure-env
[2021-01-21T19:03:38.435Z] {
[2021-01-21T19:03:38.435Z]   "AttachmentsLink": "dbs/uY8bAA==/colls/uY8bALgik0U=/docs/uY8bALgik0UeAAAAAAAAAA==/attachments/",
[2021-01-21T19:03:38.435Z]   "TimeToLive": null,
[2021-01-21T19:03:38.435Z]   "Id": "@azure|ms-rest-azure-env",
[2021-01-21T19:03:38.436Z]   "ResourceId": "uY8bALgik0UeAAAAAAAAAA==",
[2021-01-21T19:03:38.436Z]   "SelfLink": "dbs/uY8bAA==/colls/uY8bALgik0U=/docs/uY8bALgik0UeAAAAAAAAAA==/",
[2021-01-21T19:03:38.436Z]   "AltLink": "dbs/dev/colls/npm/docs/@azure|ms-rest-azure-env",
[2021-01-21T19:03:38.436Z]   "Timestamp": "2021-01-21T18:55:01Z",
[2021-01-21T19:03:38.436Z]   "ETag": "\u00225e005ff1-0000-0100-0000-6009ce050000\u0022"
[2021-01-21T19:03:38.436Z] }
[2021-01-21T19:03:38.436Z] Document Id @azure|ms-rest-js
[2021-01-21T19:03:38.436Z] {
[2021-01-21T19:03:38.436Z]   "AttachmentsLink": "dbs/uY8bAA==/colls/uY8bALgik0U=/docs/uY8bALgik0UfAAAAAAAAAA==/attachments/",
[2021-01-21T19:03:38.436Z]   "TimeToLive": null,
[2021-01-21T19:03:38.436Z]   "Id": "@azure|ms-rest-js",
[2021-01-21T19:03:38.436Z]   "ResourceId": "uY8bALgik0UfAAAAAAAAAA==",
[2021-01-21T19:03:38.436Z]   "SelfLink": "dbs/uY8bAA==/colls/uY8bALgik0U=/docs/uY8bALgik0UfAAAAAAAAAA==/",
[2021-01-21T19:03:38.436Z]   "AltLink": "dbs/dev/colls/npm/docs/@azure|ms-rest-js",
[2021-01-21T19:03:38.436Z]   "Timestamp": "2021-01-21T18:55:01Z",
[2021-01-21T19:03:38.436Z]   "ETag": "\u00225e0060f1-0000-0100-0000-6009ce050000\u0022"
[2021-01-21T19:03:38.436Z] }
[2021-01-21T19:03:38.450Z] Executed 'CosmosGremlinTrigger' (Succeeded, Id=eec855bc-b7ca-48d2-88d3-5d325d10eb91, Duration=66ms)
```


```
$ func azure functionapp publish CosmosGremlinTrigger
Microsoft (R) Build Engine version 16.8.0+126527ff1 for .NET
Copyright (C) Microsoft Corporation. All rights reserved.

  Determining projects to restore...
  All projects are up-to-date for restore.
  CosmosGremlinTrigger -> /Users/cjoakim/Projects/CosmosGremlinTrigger/bin/publish/bin/CosmosGremlinTrigger.dll

Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:02.62


Getting site publishing info...
Creating archive for current directory...
Uploading 3.98 MB [###############################################################################]
Upload completed successfully.
Deployment completed successfully.
Syncing triggers...
Functions in CosmosGremlinTrigger:
    CosmosGremlinTrigger - [cosmosDBTrigger]

```


g.V().drop()