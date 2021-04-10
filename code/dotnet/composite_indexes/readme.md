# Bulk Executor

## Links

- https://devblogs.microsoft.com/cosmosdb/introducing-bulk-support-in-the-net-sdk/
- https://docs.microsoft.com/en-us/azure/cosmos-db/tutorial-sql-api-dotnet-bulk-import
- git clone https://github.com/Azure/azure-cosmosdb-bulkexecutor-dotnet-getting-started.git


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

