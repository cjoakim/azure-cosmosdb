# CosmosDB w/DotNet 5

## Links

- https://www.nuget.org/packages/Microsoft.Azure.Cosmos/
- https://github.com/Azure/azure-cosmos-dotnet-v3
- https://github.com/AzureCosmosDB/labs
- https://github.com/AzureCosmosDB/labs/blob/master/dotnet/labs/08-change_feed_with_azure_functions.md

## DotNet Core Project Setup

```
$ dotnet --version
5.0.202

$ dotnet new console -o 

$ cd sample_console_app/

$ dotnet add package Microsoft.Azure.Cosmos                <-- this is all you need

// dotnet add package Microsoft.EntityFrameworkCore.Cosmos  <-- EF

$ dotnet add package Azure.Storage.Blobs                   <-- I often use these other libs, too
$ dotnet add package Microsoft.Azure.DataLake.Store
$ dotnet add package CsvHelper
$ dotnet add package Gremlin.Net
$ dotnet add package DocumentFormat.OpenXml
$ dotnet add package Faker.Net

$ dotnet list package
Project 'sample_console_app' has the following package references
   [net5.0]: 
   Top-level Package                     Requested   Resolved
   > Azure.Storage.Blobs                 12.9.1      12.9.1  
   > CsvHelper                           27.1.1      27.1.1  
   > DocumentFormat.OpenXml              2.13.0      2.13.0  
   > Faker.Net                           1.5.138     1.5.138 
   > Microsoft.Azure.Cosmos              3.20.0      3.20.0  
   > Microsoft.Azure.DataLake.Store      1.1.24      1.1.24  

$ dotnet restore
...

$ dotnet build
Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:01.44

$ dotnet run
Hello World!
```
